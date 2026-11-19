from events.models import Event, UpdateTracker
from events.ticketmaster.ticketmaster import fetch_events
from events.ticketmaster.processing import process_one_event

def sync_events(event_count: int, city: str, startDateTime: str, endDateTime: str):
    events = fetch_events(size=event_count, city=city, startDateTime=startDateTime, endDateTime=endDateTime)
    created = 0
    updated = 0

    for event in events:
        data = process_one_event(event)

        tm_id = data.pop("ticketmaster_id")
        _, _= Event.objects.update_or_create(
            ticketmaster_id=tm_id,
            defaults=data
        )

        