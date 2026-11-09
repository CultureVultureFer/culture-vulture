import re
import uuid

from django.db import IntegrityError, transaction

from .models import Role, User

class GoogleLoginError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def login_with_google(claims: dict, token: dict, current_user=None) -> User:
    subject = claims.get("sub")
    if not subject:
        raise GoogleLoginError("invalid_token")

    logged_in = current_user if current_user is not None and current_user.is_authenticated else None

    if logged_in:
        raise GoogleLoginError("user_already_logged_in")

    user_id = uuid.uuid5(uuid.NAMESPACE_OID, subject)
    user = User.objects.filter(pk=user_id).first()
    if user is not None:
        if not user.is_active:
            raise GoogleLoginError("account_disabled")
        return user

    email = (claims.get("email") or "").strip().lower()
    if not email or not claims.get("email_verified"):
        raise GoogleLoginError("email_not_verified")
    if User.objects.filter(email__iexact=email).exists():
        raise GoogleLoginError("email_exists")

    try:
        with transaction.atomic():
            user = User.objects.create_user(
                id=user_id,
                username=_unique_username(claims, email),
                email=email,
                password=None,
                role=Role.get(Role.USER),
                first_name=(claims.get("given_name") or "")[:150],
                last_name=(claims.get("family_name") or "")[:150],
            )
    except IntegrityError:
        raise GoogleLoginError("email_exists")
    return user


def _unique_username(claims: dict, email: str) -> str:
    base = claims.get("name") or claims.get("given_name") or email.split("@")[0]
    base = re.sub(r"[^\w .,'&()+-]", "", base).strip()[:140] or "user"
    candidate, n = base, 1
    while User.objects.filter(username__iexact=candidate).exists():
        n += 1
        candidate = f"{base} {n}"
    return candidate
