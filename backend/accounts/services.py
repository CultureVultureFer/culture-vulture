import re
import uuid

from django.db import IntegrityError, transaction

from .models import Organization, Role, User

class GoogleLoginError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def login_with_google(claims, current_user=None):
    user_id = _google_user_id(claims, current_user)

    existing = _existing_google_user(user_id)
    if existing is not None:
        return existing

    email = _new_user_email(claims)
    try:
        with transaction.atomic():
            user = _create_google_user(claims, user_id, email, Role.USER)
    except IntegrityError:
        raise GoogleLoginError("email_exists")
    return user


def register_organizer_with_google(claims, organization_name, current_user=None):
    user_id = _google_user_id(claims, current_user)

    # Kao obična prijava: postojeći račun se samo prijavi, a naziv organizacije se ignorira.
    existing = _existing_google_user(user_id)
    if existing is not None:
        return existing

    email = _new_user_email(claims)
    try:
        with transaction.atomic():
            organization = _get_or_create_organization(organization_name)
            user = _create_google_user(claims, user_id, email, Role.ORGANIZER, organization=organization)
    except IntegrityError:
        raise GoogleLoginError("email_exists")
    return user


def _existing_google_user(user_id):
    user = User.objects.filter(pk=user_id).first()
    if user is not None and not user.is_active:
        raise GoogleLoginError("account_disabled")
    return user


def _get_or_create_organization(name):
    organization = Organization.objects.filter(name__iexact=name).first()
    if organization is not None:
        return organization
    try:
        with transaction.atomic():
            return Organization.objects.create(name=name)
    except IntegrityError:
        # Netko je u istom trenutku kreirao istu organizaciju, pa se pridruži njegovoj.
        return Organization.objects.get(name__iexact=name)


def _google_user_id(claims, current_user):
    subject = claims.get("sub")
    if not subject:
        raise GoogleLoginError("invalid_token")

    if current_user is not None and current_user.is_authenticated:
        raise GoogleLoginError("user_already_logged_in")

    return uuid.uuid5(uuid.NAMESPACE_OID, subject)


def _new_user_email(claims):
    email = (claims.get("email") or "").strip().lower()
    if not email or not claims.get("email_verified"):
        raise GoogleLoginError("email_not_verified")
    if User.objects.filter(email__iexact=email).exists():
        raise GoogleLoginError("email_exists")
    return email


def _create_google_user(claims, user_id, email, role_name, organization=None):
    return User.objects.create_user(
        id=user_id,
        username=_unique_username(claims, email),
        email=email,
        password=None,
        role=Role.get(role_name),
        organization=organization,
    )


def _unique_username(claims, email):
    base = claims.get("name") or claims.get("given_name") or email.split("@")[0]
    base = re.sub(r"[^\w .,'&()+-]", "", base).strip()[:140] or "user"
    candidate, n = base, 1
    while User.objects.filter(username__iexact=candidate).exists():
        n += 1
        candidate = f"{base} {n}"
    return candidate
