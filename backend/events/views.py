from django.shortcuts import render, get_object_or_404
import httpx

from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from accounts.permissions import IsOrganizer, IsOrganizerOrReadOnly
from events.models import Category, Event, UpdateTracker
from events.serializers import CategorySerializer, EventDetailSerializer, EventSerializer
from events.ticketmaster.sync_data import sync_events


from datetime import timedelta
from django.utils import timezone

def _detailed_events():
    # Loads the organizer, their organization and the categories up front,
    # so serializing a list does not run extra queries for every event.
    return Event.objects.select_related("organizer__organization").prefetch_related("categories")


@api_view(["GET", "POST"])
@permission_classes([IsOrganizerOrReadOnly])
def events_view(request):
    # One URL, two methods: GET lists all events (F-003), POST publishes a new one (F-010).
    if request.method == "POST":
        return _create_event(request)
    return _list_events()


def _create_event(request):
    serializer = EventDetailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # The organizer always comes from the session, never from the request body.
    serializer.save(organizer=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsOrganizerOrReadOnly])
def event_detail_view(request, event_id):
    event = get_object_or_404(_detailed_events(), pk=event_id)

    if request.method == "GET":
        return Response(EventDetailSerializer(event).data)

    # F-004: only the organizer who published the event can change or delete it.
    # Imported Ticketmaster events have no organizer, so nobody can edit them here.
    if event.organizer != request.user:
        raise PermissionDenied("You can only manage your own events.")

    if request.method == "DELETE":
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # partial=True: the client may send only the fields that changed.
    serializer = EventDetailSerializer(event, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsOrganizer])
def my_events_view(request):
    events = _detailed_events().filter(organizer=request.user).order_by("start")
    return Response(EventDetailSerializer(events, many=True).data)


@api_view(["GET"])
def categories_view(request):
    categories = Category.objects.order_by("category_name")
    return Response(CategorySerializer(categories, many=True).data)

class EventListView(ListAPIView):
    queryset = Event.objects.all().order_by("start")
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]
    # F-008: ?search=<term> matches event name or organizer's organization name
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["event_name", "organizer__organization__name"]
    ordering = ["start", "event_id"]

    def list(self, request, *args, **kwargs):
        now = timezone.now()
        start_datetime = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_datetime = (now + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

        update_checks = UpdateTracker.objects.all()
        for update in update_checks:
            print(update)
            if update.next_update_datetime >= timezone.now():
                try:
                    sync_events(event_count=100, city="Berlin", startDateTime=start_datetime, endDateTime=end_datetime)
                except httpx.HTTPError:
                    return Response(
                        {"error": "Ticketmaster API error"},
                        status=status.HTTP_502_BAD_GATEWAY
                    )
                update.next_update_datetime = now + update.update_period
                update.save()
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return _create_event(request)
