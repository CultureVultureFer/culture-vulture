import math

from django.utils import timezone
from rest_framework import serializers

from accounts.models import User
from events.models import Category, Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name"]


class EventOrganizerSerializer(serializers.ModelSerializer):
    # allow_null is required, otherwise the key is left out for a user without an organization.
    organization = serializers.CharField(source="organization.name", read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ["id", "username", "organization"]


class EventDetailSerializer(serializers.ModelSerializer):
    """One event, for reading and for organizer writes (F-010 create, F-004 edit).

    Read:  categories and organizer are nested objects, is_imported tells Ticketmaster events apart.
    Write: categories are sent as category_ids. The organizer and ticketmaster_id cannot be
           written at all: the view sets the organizer from the logged-in user.
    """

    categories = CategorySerializer(many=True, read_only=True)
    # Must be declared explicitly: DRF makes a many-to-many field with a through model
    # read-only by default. Event_Categories has no extra fields, so ModelSerializer's
    # create()/update() can still save it with .set(). If Event_Categories ever gets
    # extra required fields, create()/update() have to be written by hand.
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        source="categories",
        queryset=Category.objects.all(),
        write_only=True,
        allow_empty=False,
    )
    organizer = EventOrganizerSerializer(read_only=True)
    is_imported = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "event_id",
            "event_name",
            "event_description",
            "categories",
            "category_ids",
            "start",
            "end",
            "location",
            "latitude",
            "longitude",
            "entry_price",
            "price_currency",
            "organizer",
            "is_imported",
        ]
        # These columns are nullable because Ticketmaster does not always provide them,
        # but an organizer has to fill them in.
        extra_kwargs = {
            "start": {"required": True, "allow_null": False},
            "end": {"required": True, "allow_null": False},
            "location": {"required": True, "allow_null": False, "allow_blank": False},
            "entry_price": {"min_value": 0},
        }

    def get_is_imported(self, event) -> bool:
        return event.ticketmaster_id is not None

    def validate_latitude(self, value):
        return _validate_coordinate(value, 90)

    def validate_longitude(self, value):
        return _validate_coordinate(value, 180)

    def validate(self, attrs):
        # On PATCH only the sent fields are in attrs, so rules that compare two fields
        # fall back to the values already stored on the event.
        def current(name):
            return attrs[name] if name in attrs else getattr(self.instance, name, None)

        errors = {}

        start, end = current("start"), current("end")
        if start and end and end <= start:
            errors["end"] = ["The event must end after it starts."]

        # A new event cannot start in the past. When editing, this is checked only if the
        # start is actually changed, so an event that already started can still be corrected.
        start_changed = self.instance is None or ("start" in attrs and attrs["start"] != self.instance.start)
        if start and start_changed and start <= timezone.now():
            errors["start"] = ["The event must start in the future."]

        if (current("latitude") is None) != (current("longitude") is None):
            errors["latitude"] = ["Latitude and longitude must be sent together."]

        if errors:
            raise serializers.ValidationError(errors)

        if current("entry_price") is not None and not current("price_currency"):
            attrs["price_currency"] = "EUR"
        return attrs


def _validate_coordinate(value, limit):
    # Coordinates are stored as text (same as the Ticketmaster import), so the number
    # check has to be done here. Both 45.81 and "45.81" are accepted.
    if value in (None, ""):
        return None
    try:
        number = float(value)
    except ValueError:
        raise serializers.ValidationError("A valid number is required.")
    if not math.isfinite(number) or abs(number) > limit:
        raise serializers.ValidationError(f"Must be between -{limit} and {limit}.")
    return value
