import time
from unittest import mock
from urllib.parse import parse_qs, urlparse

from django.test import TestCase, override_settings
from joserfc import jwt
from joserfc.jwk import RSAKey

from .models import Role, User
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

    def google_flow(self, client=None, state=None, **claims):
        client = client or self.client
        resp = client.get("/api/auth/google/login/")
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
