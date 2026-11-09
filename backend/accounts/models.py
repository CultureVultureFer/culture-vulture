import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.functions import Lower


class Role(models.Model):
    USER = "USER"
    ORGANIZER = "ORGANIZER"
    ADMIN = "ADMIN"
    NAME_CHOICES = [
        (USER, "User"),
        (ORGANIZER, "Organizer"),
        (ADMIN, "Admin"),
    ]

    name = models.CharField(max_length=20, unique=True, choices=NAME_CHOICES)

    def __str__(self):
        return self.get_name_display()

    @classmethod
    def get(cls, name):
        role, _ = cls.objects.get_or_create(name=name)
        return role


class UserManager(DjangoUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", Role.get(Role.USER))
        return super().create_user(username, self.normalize_email(email).lower(), password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", Role.get(Role.ADMIN))
        return super().create_superuser(username, self.normalize_email(email).lower(), password, **extra_fields)


username_validator = RegexValidator(
    regex=r"^[\w .,'&()+-]+\Z",
    message="Name may contain letters, digits, spaces and . , ' & ( ) + - _",
)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("email"), name="user_email_ci_unique"),
            models.UniqueConstraint(Lower("username"), name="user_username_ci_unique"),
        ]

    @property
    def is_organizer(self):
        return self.role.name == Role.ORGANIZER

    @property
    def is_app_admin(self):
        return self.role.name == Role.ADMIN
