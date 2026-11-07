import json
import time
from unittest import mock
from urllib.parse import parse_qs, urlparse

from django.test import Client, TestCase, override_settings
from joserfc import jwt
from joserfc.jwk import RSAKey

from .models import OAuthAccount, Role, User
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


def post_json(client, url, data, **extra):
    return client.post(url, data=json.dumps(data), content_type="application/json", **extra)


class FakeGoogleMixin:
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

    def google_flow(self, client=None, next_path=None, state=None, **claims):
        client = client or self.client
        url = "/api/auth/google/login/" + (f"?next={next_path}" if next_path else "")
        resp = client.get(url)
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
    def test_redirect_to_google_has_state_nonce_pkce(self):
        _, _, params = self.google_flow()
        self.assertEqual(params["code_challenge_method"], ["S256"])
        self.assertEqual(params["scope"], ["openid email profile"])
        for key in ("state", "nonce", "code_challenge", "redirect_uri"):
            self.assertIn(key, params)

    def test_first_google_login_registers_user(self):
        resp, sent, _ = self.google_flow()

        self.assertEqual(resp["Location"], FRONTEND + "/")
        self.assertIn("code_verifier", sent)

        user = User.objects.get()
        self.assertEqual(user.email, "marko@gmail.com")
        self.assertEqual(user.username, "Marko Marić")
        self.assertEqual(user.role.name, Role.USER)
        self.assertFalse(user.has_usable_password())

        account = OAuthAccount.objects.get()
        self.assertEqual((account.provider, account.provider_user_id), ("google", "google-sub-1"))
        self.assertEqual(account.access_token, "ya29.test")
        self.assertIsNotNone(account.token_expires_at)

        me = self.client.get("/api/auth/me/").json()
        self.assertEqual(me, {"id": user.pk, "username": "Marko Marić", "email": "marko@gmail.com", "role": "USER"})

    def test_second_google_login_reuses_user(self):
        self.google_flow()
        self.client.post("/api/auth/logout/")
        self.google_flow(email="marko.novi@gmail.com")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(OAuthAccount.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "marko@gmail.com")

    def test_login_rotates_session_key(self):
        self.client.get("/api/auth/csrf/")
        self.client.session.save()
        before = self.client.session.session_key
        self.google_flow()
        self.assertNotEqual(before, self.client.session.session_key)

    def test_username_collision_gets_suffix(self):
        self.google_flow()
        self.google_flow(client=Client(), sub="google-sub-2", email="drugi.marko@gmail.com")
        self.assertTrue(User.objects.filter(username="Marko Marić 2").exists())

    def test_superuser_email_is_not_auto_linked(self):
        User.objects.create_superuser(username="Admin", email="marko@gmail.com", password="Admin-Pass-123")
        resp, _, _ = self.google_flow()
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=email_exists")
        self.assertFalse(OAuthAccount.objects.exists())

    def test_logged_in_superuser_links_google(self):
        admin = User.objects.create_superuser(username="Admin", email="admin@example.com", password="Admin-Pass-123")
        self.client.force_login(admin)
        resp, _, _ = self.google_flow(next_path="/admin-panel")
        self.assertEqual(resp["Location"], FRONTEND + "/admin-panel")
        self.assertEqual(OAuthAccount.objects.get().user, admin)

    def test_google_linked_to_someone_else(self):
        self.google_flow()
        admin = User.objects.create_superuser(username="Admin", email="admin@example.com", password="Admin-Pass-123")
        c = Client()
        c.force_login(admin)
        resp, _, _ = self.google_flow(client=c)
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=google_linked_to_other_account")

    def test_disabled_account(self):
        self.google_flow()
        User.objects.update(is_active=False)
        resp, _, _ = self.google_flow(client=Client())
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=account_disabled")

    def test_unverified_email_rejected(self):
        resp, _, _ = self.google_flow(email_verified=False)
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=email_not_verified")
        self.assertFalse(User.objects.exists())

    def test_tampered_state_rejected(self):
        resp, _, _ = self.google_flow(state="podmetnuto")
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=oidc_error")
        self.assertFalse(User.objects.exists())

    def test_token_for_other_app_rejected(self):
        resp, _, _ = self.google_flow(aud="tudja-aplikacija")
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=oidc_error")
        self.assertFalse(User.objects.exists())

    def test_token_from_other_issuer_rejected(self):
        resp, _, _ = self.google_flow(iss="https://zlo.example")
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=oidc_error")

    def test_user_cancelled(self):
        self.client.get("/api/auth/google/login/")
        resp = self.client.get("/api/auth/google/callback/", {"error": "access_denied"})
        self.assertEqual(resp["Location"], FRONTEND + "/login?auth_error=cancelled")

    def test_open_redirect_blocked(self):
        resp, _, _ = self.google_flow(next_path="//zlo.example/phish")
        self.assertEqual(resp["Location"], FRONTEND + "/")


@override_settings(FRONTEND_URL=FRONTEND)
class OrganizerTests(FakeGoogleMixin, TestCase):
    url = "/api/auth/register/organizer/"

    def test_full_organizer_registration(self):
        resp, _, _ = self.google_flow(next_path="/register/organizer")
        self.assertEqual(resp["Location"], FRONTEND + "/register/organizer")

        resp = post_json(self.client, self.url, {"name": "Kino Europa", "email": "ignorirano@x.hr"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["role"], "ORGANIZER")
        self.assertEqual(resp.json()["username"], "Kino Europa")
        self.assertEqual(resp.json()["email"], "marko@gmail.com")
        self.assertTrue(User.objects.get().is_organizer)

    def test_requires_login(self):
        resp = post_json(self.client, self.url, {"name": "Kino Europa"})
        self.assertEqual(resp.status_code, 401)

    def test_requires_csrf(self):
        strict = Client(enforce_csrf_checks=True)
        self.google_flow(client=strict)
        self.assertEqual(post_json(strict, self.url, {"name": "Kino Europa"}).status_code, 403)

        strict.get("/api/auth/csrf/")
        token = strict.cookies["csrftoken"].value
        self.assertEqual(post_json(strict, self.url, {"name": "Kino Europa"}, HTTP_X_CSRFTOKEN=token).status_code, 200)

    def test_duplicate_name_case_insensitive(self):
        other = User.objects.create_user(username="Kino Europa", email="kino@example.com", password=None)
        self.assertIsNotNone(other.pk)
        self.google_flow()
        resp = post_json(self.client, self.url, {"name": "kino  europa"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["errors"]["name"], ["An organization with this name already exists."])

    def test_own_current_name_is_allowed(self):
        self.google_flow()
        resp = post_json(self.client, self.url, {"name": "Marko Marić"})
        self.assertEqual(resp.status_code, 200)

    def test_invalid_characters(self):
        self.google_flow()
        resp = post_json(self.client, self.url, {"name": "<script>"})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("name", resp.json()["errors"])

    def test_missing_name(self):
        self.google_flow()
        resp = post_json(self.client, self.url, {})
        self.assertEqual(set(resp.json()["errors"]), {"name"})

    def test_cannot_become_organizer_twice(self):
        self.google_flow()
        post_json(self.client, self.url, {"name": "Kino Europa"})
        resp = post_json(self.client, self.url, {"name": "Kino Zagreb"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(User.objects.get().username, "Kino Europa")

    def test_admin_cannot_become_organizer(self):
        admin = User.objects.create_superuser(username="Admin", email="admin@example.com", password="Admin-Pass-123")
        self.client.force_login(admin)
        resp = post_json(self.client, self.url, {"name": "Kino Europa"})
        self.assertEqual(resp.status_code, 400)
        admin.refresh_from_db()
        self.assertTrue(admin.is_app_admin)


class SessionTests(TestCase):
    def test_me_anonymous(self):
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)

    def test_logout(self):
        user = User.objects.create_user(username="ana", email="ana@example.com", password=None)
        self.client.force_login(user)
        self.assertEqual(self.client.post("/api/auth/logout/").status_code, 204)
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)

    def test_logout_rejects_get(self):
        self.assertEqual(self.client.get("/api/auth/logout/").status_code, 405)

    def test_password_endpoints_do_not_exist(self):
        body = {"email": "ana@example.com", "password": "Kultura-2026!", "username": "ana"}
        self.assertEqual(post_json(self.client, "/api/auth/login/", body).status_code, 404)
        self.assertEqual(post_json(self.client, "/api/auth/register/", body).status_code, 404)
        self.assertFalse(User.objects.exists())


class RoleSetupTests(TestCase):
    def test_roles_seeded_by_migration(self):
        self.assertEqual(set(Role.objects.values_list("name", flat=True)), {"USER", "ORGANIZER", "ADMIN"})

    def test_superuser_gets_admin_role(self):
        admin = User.objects.create_superuser(username="Admin", email="admin@example.com", password="Admin-Pass-123")
        self.assertTrue(admin.is_app_admin)
