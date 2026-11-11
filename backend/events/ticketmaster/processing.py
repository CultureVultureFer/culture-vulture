from events.models import Event
from events.ticketmaster.ticketmaster import fetch_events
from django.utils.dateparse import parse_datetime

def process_one_event(event):
    ticketmaster_id = event.get("id")
    event_name = event.get("name")
    event_description = event.get("info")
    start = event.get("dates", {}).get("start", {}).get("dateTime")
    end = event.get("dates", {}).get("end", {}).get("dateTime")

    start = parse_datetime(start) if start else None
    end = parse_datetime(end) if end else None

    venue = event.get("_embedded", {}).get("venues", [])[0]
    place = event.get("place", {})

    origin = venue if venue else place

    address = origin.get("address", {})
    city = origin.get("city", {})
    place_name = origin.get("name")
    line1 = address.get("line1")
    city_name = city.get("name")

    parts_tmp = [place_name, line1, city_name]
    parts = filter(None, parts_tmp)
    
    location = ", ".join(parts)
    coordinates = origin.get("location", {})

    latitude = coordinates.get("latitude")
    longitude = coordinates.get("longitude")

    latitude = str(latitude) if latitude is not None else None
    longitude = str(longitude) if longitude is not None else None

    price_range = event.get("priceRanges", [])
    entry_price = price_range[0].get("min") if price_range else None

    currency = price_range[0].get("currency") if price_range else None

    return {
        "ticketmaster_id": ticketmaster_id,
        "event_name": event_name,
        "event_description": event_description,
        "organizer": None,
        "start": start,
        "end": end,
        "location": location or None,
        "latitude": latitude,
        "longitude": longitude,
        "entry_price": entry_price,
        "price_currency": currency,
    }
