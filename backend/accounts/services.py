"""
Poslovna logika registracije i prijave (F-001), odvojena od HTTP-a.

View (views.py) zna za zahtjeve, kolačiće i redirecte; ovdje su samo pravila
"tko smije dobiti koji račun". Tako se pravila testiraju bez HTTP-a.
"""

import re
from datetime import UTC, datetime

from django.db import IntegrityError, transaction

from .models import OAuthAccount, Role, User


# ------------------------------------------------------------------------------
# Postajanje organizatorom
# ------------------------------------------------------------------------------

class OrganizerError(Exception):
    """Korisnik ne može postati organizator (npr. već jest)."""


def become_organizer(user: User, organization_name: str) -> User:
    """
    Pretvori prijavljenog korisnika (USER) u organizatora.

    Organizator se registrira u dva koraka:
      1. prijava Googleom (kao i svi ostali) -> račun s ulogom USER,
      2. ovaj korak: upiše naziv organizacije -> uloga ORGANIZER,
         a `username` postaje naziv organizacije (prikazuje se uz događaje).

    Dopušteno je samo iz uloge USER: administrator se ne smije "spustiti"
    u organizatora, a organizator ne treba ovaj korak dvaput.

    Sada se svatko može proglasiti organizatorom. Ako tim odluči da
    organizatore odobrava administrator, ovdje se umjesto ORGANIZER postavlja
    npr. zasebna oznaka "čeka odobrenje", a admin je mijenja u /admin.

    Baca IntegrityError ako je netko u istom trenutku zauzeo isti naziv;
    view to pretvara u grešku 400.
    """
    if user.role.name != Role.USER:
        raise OrganizerError(f"Account already has the role {user.role.name}.")

    with transaction.atomic():
        user.username = organization_name
        user.role = Role.get(Role.ORGANIZER)
        user.save(update_fields=["username", "role"])
    return user


# ------------------------------------------------------------------------------
# Prijava Googleom (OpenID Connect)
# ------------------------------------------------------------------------------

class GoogleLoginError(Exception):
    """Google je potvrdio identitet, ali prijavu ne dopuštamo."""

    def __init__(self, code: str):
        super().__init__(code)
        # Kratak kod koji frontend prevodi u poruku (?auth_error=<code>).
        self.code = code


def login_with_google(claims: dict, token: dict, current_user=None) -> User:
    """
    Vrati korisnika za provjeren id_token (claims) s Googlea.

    Ovo je JEDINI način registracije i prijave u aplikaciju.

    Tri slučaja:
      1. Google račun je već povezan  -> prijavi tog korisnika.
      2. Korisnik je VEĆ prijavljen (npr. superuser preko /admin) -> poveži
         Google s njegovim računom.
      3. Nitko nije prijavljen i račun ne postoji -> registriraj novog
         korisnika s ulogom USER, bez lozinke. Organizatorom postaje kasnije
         (become_organizer).

    Ako već postoji račun s tim emailom, a bez povezanog Googlea (to može
    biti samo superuser napravljen naredbom createsuperuser), NE povezujemo
    ga automatski nego vraćamo "email_exists". Takav račun nije nastao
    Googleom, pa nemamo dokaz da pripada istoj osobi; povezuje se tako da se
    vlasnik prvo prijavi u /admin, pa Googleom (slučaj 2).

    claims moraju doći iz id_tokena kojem je Authlib provjerio potpis.
    """
    subject = claims.get("sub")
    if not subject:
        raise GoogleLoginError("invalid_token")

    logged_in = current_user if current_user is not None and current_user.is_authenticated else None

    account = (
        OAuthAccount.objects.select_related("user")
        .filter(provider=OAuthAccount.GOOGLE, provider_user_id=subject)
        .first()
    )

    # 1. Već povezan Google račun
    if account is not None:
        if logged_in and account.user_id != logged_in.pk:
            raise GoogleLoginError("google_linked_to_other_account")
        if not account.user.is_active:
            # F-007: "nakon brisanja profila korisnik se više ne može
            # prijaviti". Brisanje profila zato treba biti is_active=False.
            raise GoogleLoginError("account_disabled")
        _save_tokens(account, token)
        return account.user

    # 2. Povezivanje s trenutno prijavljenim korisnikom
    if logged_in:
        if logged_in.oauth_accounts.filter(provider=OAuthAccount.GOOGLE).exists():
            raise GoogleLoginError("other_google_already_linked")
        _create_account(logged_in, subject, token)
        return logged_in

    # 3. Novi korisnik
    # Email je kod nas obavezan i jedinstven, pa ga uzimamo samo ako ga je
    # Google potvrdio. Nepotvrđen email bi mogao biti tuđ.
    email = (claims.get("email") or "").strip().lower()
    if not email or not claims.get("email_verified"):
        raise GoogleLoginError("email_not_verified")
    if User.objects.filter(email__iexact=email).exists():
        raise GoogleLoginError("email_exists")

    try:
        with transaction.atomic():
            user = User.objects.create_user(
                username=_unique_username(claims, email),
                email=email,
                password=None,  # -> set_unusable_password(): prijava lozinkom nije moguća
                role=Role.get(Role.USER),
                first_name=(claims.get("given_name") or "")[:150],
                last_name=(claims.get("family_name") or "")[:150],
            )
            _create_account(user, subject, token)
    except IntegrityError:
        # Dva istovremena callbacka za istog korisnika (dvostruki klik):
        # drugi naiđe na unique constraint, pa vraćamo onog prvog.
        account = OAuthAccount.objects.select_related("user").filter(
            provider=OAuthAccount.GOOGLE, provider_user_id=subject
        ).first()
        if account is None:
            # Sudar na emailu ili imenu, ne na Google računu.
            raise GoogleLoginError("email_exists") from None
        return account.user
    return user


def _create_account(user: User, subject: str, token: dict) -> OAuthAccount:
    account = OAuthAccount(user=user, provider=OAuthAccount.GOOGLE, provider_user_id=subject)
    _save_tokens(account, token, commit=False)
    account.save()
    return account


def _save_tokens(account: OAuthAccount, token: dict, commit: bool = True) -> None:
    account.access_token = token.get("access_token", "")
    # Google refresh token šalje samo pri prvom pristanku (i samo uz
    # access_type=offline). Ako ga sada nema, NE brišemo stari.
    if token.get("refresh_token"):
        account.refresh_token = token["refresh_token"]
    expires_at = token.get("expires_at")
    account.token_expires_at = datetime.fromtimestamp(expires_at, tz=UTC) if expires_at else None
    account.scope = token.get("scope", "")
    account.token_type = token.get("token_type", "")
    if commit:
        account.save()


def _unique_username(claims: dict, email: str) -> str:
    """
    Google korisnik ne bira ime pri registraciji, pa ga predložimo iz imena
    na Google računu (ili iz emaila) i dodamo broj ako je zauzeto.
    Korisnik ga kasnije može promijeniti (F-007).
    """
    base = claims.get("name") or claims.get("given_name") or email.split("@")[0]
    base = re.sub(r"[^\w .,'&()+-]", "", base).strip()[:140] or "user"
    candidate, n = base, 1
    while User.objects.filter(username__iexact=candidate).exists():
        n += 1
        candidate = f"{base} {n}"
    return candidate
