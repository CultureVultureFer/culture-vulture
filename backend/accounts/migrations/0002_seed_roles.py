from django.db import migrations

ROLES = ["USER", "ORGANIZER", "ADMIN"]


def create_roles(apps, schema_editor):
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
