from django.shortcuts import render
import httpx

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from events.models import Event
from events.serializers import EventSerializer
from events.ticketmaster.sync_data import sync_events

@api_view(["GET"])
def get_events(req):
    try:
        sync_events()
    except httpx.HTTPError:
        return Response(
            {"error": "Ticketmaster API error"},
            status=status.HTTP_502_BAD_GATEWAY
        )
    events = Event.objects.all().order_by("start")

    serializer = EventSerializer(events, many = True)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
    
