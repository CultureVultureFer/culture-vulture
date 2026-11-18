from django.core.management.base import BaseCommand
from events.ticketmaster.sync_data import sync_events
from datetime import datetime, timedelta, timezone
from events.models import UpdateTracker

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = datetime.now(timezone.utc)
        start_datetime = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_datetime = (now + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
        sync_events(event_count=100, city="Berlin", startDateTime=start_datetime, endDateTime=end_datetime)

        UpdateTracker.objects.update_or_create(
            update_period = timedelta(minutes=10),
            defaults = {
                "next_update_datetime" : (now + timedelta(hours = 1))
            }
        )
        