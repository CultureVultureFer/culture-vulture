from authlib.integrations.django_client import OAuth
from django.conf import settings

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.OIDC_GOOGLE_CLIENT_ID,
    client_secret=settings.OIDC_GOOGLE_CLIENT_SECRET,
    server_metadata_url=settings.OIDC_GOOGLE_DISCOVERY_URL,
    client_kwargs={
        "scope": "openid email profile",
        "code_challenge_method": "S256",  # PKCE
    },
)

google = oauth.google
