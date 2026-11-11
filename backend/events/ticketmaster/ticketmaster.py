import os
import httpx

from dotenv import load_dotenv

load_dotenv()
API_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def fetch_events(size: int):
    key = os.getenv("TICKETMASTER_API_KEY")
    params = {
        "apikey": key,
        "city": "Berlin",
        "size": size
    }

    res = httpx.get(API_URL, params=params, timeout=10.0)

    res.raise_for_status()

    data = res.json()
    events = data.get("_embedded", {}).get("events", [])
    return events