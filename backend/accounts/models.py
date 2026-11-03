"""
Modeli za F-001, usklađeni s ERD-om (docs/puml/4-2-culturevulture-data-ERD.puml).

ERD                  -> ovdje
-------------------     -----------------------------------------------------
ROLE                 -> Role
USER                 -> User (Djangov AbstractUser + email za prijavu + role)
  created_at         -> User.date_joined (Django ga već ima, ne dupliciramo)
OAUTH_ACCOUNTS       -> OAuthAccount
SESSIONS             -> NEMA modela: koristimo Djangove sesije (tablica
                        django_session), koje već rade sve što je ERD tražio
                        (token u kolačiću, istek, veza na korisnika).
"""

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.functions import Lower


class Role(models.Model):
    """
    Uloga korisnika (ERD: ROLE).

    Zasebna tablica (kao u ERD-u) umjesto polja s choices:
      - PREDNOST: uloge su podaci u bazi, admin ih vidi i dodjeljuje u /admin.
      - NEDOSTATAK: svaka provjera uloge je JOIN ili dodatni upit. Zato je
        `user.role` dohvaćen preko select_related gdje god je to bitno.
    Tri uloge se stvaraju migracijom 0002_seed_roles, ne ručno.
    """

    USER = "USER"
    ORGANIZER = "ORGANIZER"
    ADMIN = "ADMIN"
    NAME_CHOICES = [
        (USER, "Korisnik"),
        (ORGANIZER, "Organizator"),
        (ADMIN, "Administrator"),
    ]

    name = models.CharField(max_length=20, unique=True, choices=NAME_CHOICES)

    def __str__(self):
        return self.get_name_display()

    @classmethod
    def get(cls, name: str) -> "Role":
        return cls.objects.get(name=name)


class UserManager(DjangoUserManager):
    """
    Djangov manager uz automatsku dodjelu uloge.

    Bez ovoga `createsuperuser` ne bi radio: role je obavezan, a Django za
    njega ne zna. Obični korisnik dobiva USER, superuser dobiva ADMIN.
    """

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", Role.get(Role.USER))
        return super().create_user(username, self.normalize_email(email).lower(), password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", Role.get(Role.ADMIN))
        return super().create_superuser(username, self.normalize_email(email).lower(), password, **extra_fields)


# Djangov zadani validator ne dopušta razmake, a naziv organizacije ih ima
# ("Kino Europa", "HNK Zagreb"). Ovaj dopušta slova (i č, ć, ž...), brojke,
# razmake i uobičajene znakove u nazivima.
username_validator = RegexValidator(
    regex=r"^[\w .,'&()+-]+\Z",
    message="Name may contain letters, digits, spaces and . , ' & ( ) + - _",
)


class User(AbstractUser):
    """
    Korisnik aplikacije, za sve tri uloge (ERD: USER).

    Registracija i prijava su SAMO preko Googlea (OAuthAccount), pa korisnici
    nemaju lozinku (has_usable_password() je False). Jedina iznimka je
    superuser iz `createsuperuser`, čija lozinka služi samo za /admin.

    `email` je jedinstven i dolazi s Googlea (potvrđen). USERNAME_FIELD je
    email jer se po njemu superuser prijavljuje u /admin.
    `username` je ime koje se prikazuje: za korisnika ime s Google profila
    (može ga promijeniti, F-007), za organizatora naziv organizacije.
    """

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={"unique": "This name is already taken."},
    )
    email = models.EmailField(
        unique=True,
        error_messages={"unique": "An account with this email already exists."},
    )
    # PROTECT: uloga se ne može obrisati dok je netko ima.
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # Što `createsuperuser` traži uz email i lozinku.
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        constraints = [
            # unique=True gore razlikuje velika i mala slova ("Ana@x.hr" i
            # "ana@x.hr" bi bila dva računa). Ova ograničenja to sprječavaju
            # na razini baze, čak i ako netko zaobiđe naše forme.
            models.UniqueConstraint(Lower("email"), name="user_email_ci_unique"),
            models.UniqueConstraint(Lower("username"), name="user_username_ci_unique"),
        ]

    @property
    def is_organizer(self) -> bool:
        return self.role.name == Role.ORGANIZER

    @property
    def is_app_admin(self) -> bool:
        # Uloga ADMIN u aplikaciji. Nije isto što i is_staff (pristup /admin),
        # iako superuser ima oboje.
        return self.role.name == Role.ADMIN


class OAuthAccount(models.Model):
    """
    Vanjski račun povezan s korisnikom (ERD: OAUTH_ACCOUNTS).

    Zašto zasebna tablica, a ne polje na Useru: jedan korisnik može imati više
    providera (danas Google, sutra npr. Microsoft), a tokeni pripadaju
    providerovom računu, ne korisniku.

    TOKENI: za samu prijavu NE trebaju nam (identitet dolazi iz id_tokena).
    Spremamo ih jer ERD to predviđa i jer će F-009 (Google kalendar) trebati
    access/refresh token. Tada:
      - treba tražiti dodatni scope i `access_type=offline` za refresh token,
      - tokene bi trebalo šifrirati u bazi (npr. django-fernet-fields), jer je
        refresh token dugotrajan pristup korisnikovom Google računu.
    Sa scopeom koji sada tražimo (openid email profile) access token daje samo
    osnovne podatke profila, pa je čuvanje u čistom tekstu prihvatljivo.
    """

    GOOGLE = "google"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="oauth_accounts")
    provider = models.CharField(max_length=32)
    # Za OIDC je ovo `sub` iz id_tokena: trajan i jedinstven kod providera.
    # NIKAD email: email se mijenja i nije dokaz identiteta.
    provider_user_id = models.CharField(max_length=255)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    scope = models.TextField(blank=True)
    token_type = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OAuth account"
        constraints = [
            # Isti Google račun ne može biti povezan s dva korisnika.
            models.UniqueConstraint(fields=["provider", "provider_user_id"], name="oauth_provider_uid_unique"),
            # Jedan korisnik ima najviše jedan račun po provideru.
            models.UniqueConstraint(fields=["user", "provider"], name="oauth_user_provider_unique"),
        ]

    def __str__(self):
        return f"{self.provider}:{self.provider_user_id} -> {self.user_id}"
