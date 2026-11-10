import json
import time
from unittest import mock
from urllib.parse import parse_qs, urlparse

from django.test import TestCase, override_settings
from joserfc import jwt
from joserfc.jwk import RSAKey

from .models import Organization, Role, User
from .oidc import google

FRONTEND = "http://localhost:5173"

ISSUER = "https://accounts.google.com"
CLIENT_ID = "test-client-id"
_KEY = RSAKey.generate_key(2048, parameters={"kid": "test", "use": "sig", "alg": "RS256"})
FAKE_METADATA = {
    "issuer": ISSUER,
    "authorization_endpoint": f"{ISSUER}/o/oauth2/v2/auth",
    "token_endpoint": "https://oauth2.googleapis.com/token",
    "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
    "jwks": {"keys": [_KEY.as_dict(private=False)]},
    "_loaded_at": time.time(),
}


def make_id_token(nonce, **claims):
    now = int(time.time())
    payload = {
        "iss": ISSUER, "aud": CLIENT_ID, "iat": now, "exp": now + 300, "nonce": nonce,
        "sub": "google-sub-1", "email": "marko@gmail.com", "email_verified": True,
        "name": "Marko Marić", "given_name": "Marko", "family_name": "Marić",
        **claims,
    }
    return jwt.encode({"alg": "RS256", "kid": "test"}, payload, _KEY)


class FakeGoogleMixin(TestCase):
    def setUp(self):
        super().setUp()
        self._saved = (google.client_id, dict(google.server_metadata))
        google.client_id = CLIENT_ID
        google.server_metadata.clear()
        google.server_metadata.update(FAKE_METADATA)

    def tearDown(self):
        google.client_id = self._saved[0]
        google.server_metadata.clear()
        google.server_metadata.update(self._saved[1])
        super().tearDown()

    def google_flow(self, client=None, state=None, login_url="/api/auth/google/login/", **claims):
        client = client or self.client
        resp = client.get(login_url)
        self.assertEqual(resp.status_code, 302)
        params = parse_qs(urlparse(resp["Location"]).query)

        id_token = make_id_token(params["nonce"][0], **claims)
        sent = {}

        def fake_token_endpoint(**kwargs):
            sent.update(kwargs)
            return {"access_token": "ya29.test", "token_type": "Bearer", "expires_at": int(time.time()) + 3600,
                    "scope": "openid email profile", "id_token": id_token}

        with mock.patch.object(google, "fetch_access_token", side_effect=fake_token_endpoint):
            resp = client.get("/api/auth/google/callback/", {"code": "c0de", "state": state or params["state"][0]})
        return resp, sent, params


@override_settings(FRONTEND_URL=FRONTEND)
class GoogleLoginTests(FakeGoogleMixin, TestCase):
    def test_first_google_login_registers_user(self):
        resp, _, _ = self.google_flow()

        self.assertEqual(resp["Location"], FRONTEND + "/hello")

        user = User.objects.get()
        self.assertEqual(user.email, "marko@gmail.com")
        self.assertEqual(user.username, "Marko Marić")
        self.assertEqual(user.role.name, Role.USER)
        self.assertFalse(user.has_usable_password())

        me = self.client.get("/api/auth/me/").json()
        self.assertEqual(me, {"id": str(user.pk), "username": "Marko Marić", "email": "marko@gmail.com", "role": "USER"})

    def test_second_google_login_reuses_user(self):
        self.google_flow()
        self.client.post("/api/auth/logout/")
        self.google_flow(email="marko.novi@gmail.com")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "marko@gmail.com")

    def test_superuser_email_is_not_auto_linked(self):
        User.objects.create_superuser(username="Admin", email="marko@gmail.com", password="Admin-Pass-123")
        resp, _, _ = self.google_flow()
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=email_exists")

    def test_unverified_email_rejected(self):
        resp, _, _ = self.google_flow(email_verified=False)
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=email_not_verified")
        self.assertFalse(User.objects.exists())

    def test_tampered_state_rejected(self):
        resp, _, _ = self.google_flow(state="podmetnuto")
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=oidc_error")
        self.assertFalse(User.objects.exists())


class SessionTests(TestCase):
    def test_me_anonymous(self):
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)

    def test_logout(self):
        user = User.objects.create_user(username="ana", email="ana@example.com", password=None)
        self.client.force_login(user)
        self.assertEqual(self.client.post("/api/auth/logout/").status_code, 204)
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)


class OrganizationRegisterTests(TestCase):
    URL = "/api/auth/organization/register/"

    def register(self, body):
        data = body if isinstance(body, str) else json.dumps(body)
        return self.client.post(self.URL, data=data, content_type="application/json")

    def test_valid_name_is_stored_in_session(self):
        resp = self.register({"name": "  Klub Močvara  "})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"redirect": "/api/auth/organization/register/"})
        self.assertEqual(self.client.session["auth_intent"], "organization")
        self.assertEqual(self.client.session["pending_organization_name"], "Klub Močvara")
        self.assertFalse(Organization.objects.exists())

    def test_existing_organization_name_accepted(self):
        Organization.objects.create(name="Klub Močvara")
        resp = self.register({"name": "KLUB MOČVARA"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.client.session["pending_organization_name"], "KLUB MOČVARA")

    def test_missing_or_empty_name_rejected(self):
        for body in ({}, {"name": ""}, {"name": "   "}):
            resp = self.register(body)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.json(), {"errors": {"name": ["This field is required."]}})

    def test_invalid_characters_rejected(self):
        resp = self.register({"name": "<script>"})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("name", resp.json()["errors"])
        self.assertNotIn("pending_organization_name", self.client.session)

    def test_too_long_name_rejected(self):
        resp = self.register({"name": "x" * 151})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("name", resp.json()["errors"])

    def test_invalid_json_rejected(self):
        for body in ("not json", '["Klub"]'):
            resp = self.register(body)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp.json(), {"errors": {"__all__": ["Invalid JSON."]}})

    def test_logged_in_user_rejected(self):
        user = User.objects.create_user(username="ana", email="ana@example.com")
        self.client.force_login(user)
        resp = self.register({"name": "Klub Močvara"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {"errors": {"__all__": ["You already have an account."]}})

    def test_other_methods_not_allowed(self):
        self.assertEqual(self.client.put(self.URL).status_code, 405)


@override_settings(FRONTEND_URL=FRONTEND)
class OrganizerGoogleRegistrationTests(FakeGoogleMixin, TestCase):
    REGISTER_URL = "/api/auth/organization/register/"
    SECOND = {"sub": "google-sub-2", "email": "ivan@gmail.com", "name": "Ivan Ivić"}

    def register_name(self, name="Klub Močvara"):
        resp = self.client.post(self.REGISTER_URL, data=json.dumps({"name": name}), content_type="application/json")
        self.assertEqual(resp.status_code, 200)

    def organization_flow(self, **claims):
        return self.google_flow(login_url=self.REGISTER_URL, **claims)

    def assert_session_cleared(self):
        self.assertNotIn("auth_intent", self.client.session)
        self.assertNotIn("pending_organization_name", self.client.session)

    def test_new_name_creates_organization(self):
        self.register_name()
        resp, _, _ = self.organization_flow()

        self.assertEqual(resp["Location"], FRONTEND + "/hello")
        user = User.objects.get()
        self.assertEqual(user.email, "marko@gmail.com")
        self.assertEqual(user.username, "Marko Marić")
        self.assertEqual(user.role.name, Role.ORGANIZER)
        self.assertEqual(user.organization.name, "Klub Močvara")
        self.assertFalse(user.has_usable_password())
        self.assert_session_cleared()
        self.assertEqual(self.client.get("/api/auth/me/").json()["role"], "ORGANIZER")

    def test_existing_name_joins_organization(self):
        organization = Organization.objects.create(name="Klub Močvara")
        self.register_name("klub MOČVARA")
        resp, _, _ = self.organization_flow()

        self.assertEqual(resp["Location"], FRONTEND + "/hello")
        user = User.objects.get()
        self.assertEqual(user.role.name, Role.ORGANIZER)
        self.assertEqual(user.organization, organization)
        self.assertEqual(Organization.objects.count(), 1)
        organization.refresh_from_db()
        self.assertEqual(organization.name, "Klub Močvara")  # zadržava se izvorni naziv

    def test_organization_can_have_many_organizers(self):
        self.register_name()
        self.organization_flow()
        self.client.post("/api/auth/logout/")

        self.register_name("Klub Močvara")
        self.organization_flow(**self.SECOND)

        organization = Organization.objects.get()
        self.assertEqual(
            set(organization.organizers.values_list("email", flat=True)),
            {"marko@gmail.com", "ivan@gmail.com"},
        )

    def test_organization_created_while_on_google_is_joined(self):
        self.register_name()
        organization = Organization.objects.create(name="KLUB MOČVARA")

        resp, _, _ = self.organization_flow()
        self.assertEqual(resp["Location"], FRONTEND + "/hello")
        self.assertEqual(User.objects.get().organization, organization)
        self.assertEqual(Organization.objects.count(), 1)

    def test_organizer_logs_in_with_normal_login(self):
        self.register_name()
        self.organization_flow()
        self.client.post("/api/auth/logout/")

        resp, _, _ = self.google_flow()
        self.assertEqual(resp["Location"], FRONTEND + "/hello")
        self.assertEqual(self.client.get("/api/auth/me/").json()["role"], "ORGANIZER")
        self.assertEqual(User.objects.count(), 1)

    def test_registration_google_step_without_name(self):
        resp = self.client.get(self.REGISTER_URL)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=organization_not_registered")

    def test_existing_user_just_logs_in(self):
        self.google_flow()
        self.client.post("/api/auth/logout/")

        self.register_name()
        resp, _, _ = self.organization_flow()
        self.assertEqual(resp["Location"], FRONTEND + "/hello")
        user = User.objects.get()
        self.assertEqual(user.role.name, Role.USER)
        self.assertIsNone(user.organization)
        self.assertFalse(Organization.objects.exists())
        self.assertEqual(self.client.get("/api/auth/me/").json()["email"], "marko@gmail.com")
        self.assert_session_cleared()

    def test_existing_organizer_just_logs_in(self):
        self.register_name("Klub Močvara")
        self.organization_flow()
        self.client.post("/api/auth/logout/")

        self.register_name("Neki Drugi Klub")
        resp, _, _ = self.organization_flow()
        self.assertEqual(resp["Location"], FRONTEND + "/hello")
        self.assertEqual(User.objects.get().organization.name, "Klub Močvara")
        self.assertEqual(Organization.objects.count(), 1)

    def test_disabled_account_rejected(self):
        self.google_flow()
        self.client.post("/api/auth/logout/")
        User.objects.update(is_active=False)

        self.register_name()
        resp, _, _ = self.organization_flow()
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=account_disabled")
        self.assertFalse(Organization.objects.exists())

    def test_email_used_by_other_account_rejected(self):
        User.objects.create_superuser(username="Admin", email="marko@gmail.com", password="Admin-Pass-123")
        self.register_name()
        resp, _, _ = self.organization_flow()
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=email_exists")
        self.assertFalse(Organization.objects.exists())

    def test_unverified_email_rejected(self):
        self.register_name()
        resp, _, _ = self.organization_flow(email_verified=False)
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=email_not_verified")
        self.assertFalse(User.objects.exists())
        self.assertFalse(Organization.objects.exists())

    def test_normal_login_after_abandoned_registration(self):
        self.register_name()
        self.client.get(self.REGISTER_URL)  # korisnik je otišao na Google i nikad se nije vratio

        resp, _, _ = self.google_flow()
        self.assertEqual(resp["Location"], FRONTEND + "/hello")
        user = User.objects.get()
        self.assertEqual(user.role.name, Role.USER)
        self.assertIsNone(user.organization)
        self.assertFalse(Organization.objects.exists())
        self.assert_session_cleared()

    def test_registration_values_used_only_once(self):
        self.register_name()
        self.organization_flow(state="podmetnuto")  # i neuspjeli pokušaj čisti sesiju
        self.assert_session_cleared()
        self.assertFalse(User.objects.exists())
