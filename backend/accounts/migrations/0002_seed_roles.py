"""
Podatkovna migracija: stvara tri uloge iz README-a.

Zašto migracija, a ne ručni unos u /admin: uloge moraju postojati kod svakog
člana tima, u testovima i na serveru. Migracija se izvodi automatski uz
`migrate`, pa nitko ne mora ništa dodavati ručno.
"""

from django.db import migrations

ROLES = ["USER", "ORGANIZER", "ADMIN"]


def create_roles(apps, schema_editor):
    # apps.get_model, a ne izravan import modela: migracija mora raditi s
    # verzijom modela iz trenutka migracije, čak i kad se model kasnije promijeni.
    Role = apps.get_model("accounts", "Role")
    for name in ROLES:
        Role.objects.get_or_create(name=name)


def delete_roles(apps, schema_editor):
    Role = apps.get_model("accounts", "Role")
    Role.objects.filter(name__in=ROLES, users__isnull=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_roles, delete_roles),
    ]
