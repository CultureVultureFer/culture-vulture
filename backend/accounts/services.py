import re
from datetime import UTC, datetime

from django.db import IntegrityError, transaction

from .models import OAuthAccount, Role, User

class OrganizerError(Exception):
    pass


def become_organizer(user: User, organization_name: str) -> User:
    if user.role.name != Role.USER:
        raise OrganizerError(f"Account already has the role {user.role.name}.")

    with transaction.atomic():
        user.username = organization_name
        user.role = Role.get(Role.ORGANIZER)
        user.save(update_fields=["username", "role"])
    return user


class GoogleLoginError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def login_with_google(claims: dict, token: dict, current_user=None) -> User:
    subject = claims.get("sub")
    if not subject:
        raise GoogleLoginError("invalid_token")

    logged_in = current_user if current_user is not None and current_user.is_authenticated else None

    account = (
        OAuthAccount.objects.select_related("user")
        .filter(provider=OAuthAccount.GOOGLE, provider_user_id=subject)
        .first()
    )

    if account is not None:
        if logged_in and account.user_id != logged_in.pk:
            raise GoogleLoginError("google_linked_to_other_account")
        if not account.user.is_active:
            raise GoogleLoginError("account_disabled")
        _save_tokens(account, token)
        return account.user

    if logged_in:
        if logged_in.oauth_accounts.filter(provider=OAuthAccount.GOOGLE).exists():
            raise GoogleLoginError("other_google_already_linked")
        _create_account(logged_in, subject, token)
        return logged_in

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
                password=None,
                role=Role.get(Role.USER),
                first_name=(claims.get("given_name") or "")[:150],
                last_name=(claims.get("family_name") or "")[:150],
            )
            _create_account(user, subject, token)
    except IntegrityError:
        account = OAuthAccount.objects.select_related("user").filter(
            provider=OAuthAccount.GOOGLE, provider_user_id=subject
        ).first()
        if account is None:
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
    if token.get("refresh_token"):
        account.refresh_token = token["refresh_token"]
    expires_at = token.get("expires_at")
    account.token_expires_at = datetime.fromtimestamp(expires_at, tz=UTC) if expires_at else None
    account.scope = token.get("scope", "")
    account.token_type = token.get("token_type", "")
    if commit:
        account.save()


def _unique_username(claims: dict, email: str) -> str:
    base = claims.get("name") or claims.get("given_name") or email.split("@")[0]
    base = re.sub(r"[^\w .,'&()+-]", "", base).strip()[:140] or "user"
    candidate, n = base, 1
    while User.objects.filter(username__iexact=candidate).exists():
        n += 1
        candidate = f"{base} {n}"
    return candidate
