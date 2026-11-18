import django.db.models.deletion
from django.db import migrations, models

# Categories an organizer can pick when publishing an event (same list as the home page design).
CATEGORY_NAMES = ["music", "sport", "theatre", "education", "festivals"]


def seed_categories(apps, schema_editor):
    Category = apps.get_model("events", "Category")
    for name in CATEGORY_NAMES:
        # get_or_create keeps categories that someone already added by hand.
        Category.objects.get_or_create(category_name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event'),
        ),
        migrations.AlterField(
            model_name='event_categories',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event'),
        ),
        # Nothing to undo: the categories may already be used by events.
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
