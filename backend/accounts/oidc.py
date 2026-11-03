"""
OpenID Connect klijent za Google.

Authlib iz discovery URL-a sam dohvaća adrese providera i javne ključeve
(JWKS) za provjeru potpisa id_tokena. Za nas radi i sve sigurnosne korake:
  - state: štiti callback od CSRF-a,
  - nonce: štiti od ponovnog korištenja ukradenog id_tokena,
  - PKCE:  ukradeni `code` je bez code_verifiera beskoristan,
  - provjeru id_tokena: potpis, iss, aud (naš client_id), exp, nonce.
Ništa od toga ne pišemo ručno.

Zašto Authlib, a ne django-allauth: allauth donosi i registraciju lozinkom,
potvrde emaila, gotove forme... praktično, ali to bi bio drugi, veći sustav uz
naše JSON view-ove. Authlib rješava samo OIDC i ostavlja nam kontrolu.
Ako tim kasnije želi potvrdu emaila i "zaboravljenu lozinku" bez pisanja
vlastitog koda, allauth (headless način rada) je dobar kandidat.
"""

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
