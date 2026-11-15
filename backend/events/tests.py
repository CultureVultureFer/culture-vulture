from datetime import timedelta
from unittest import mock

from django.test import Client, TestCase
from django.utils import timezone

from accounts.models import Organization, Role, User

from .models import Category, Comments, Event, Event_Categories

EVENTS_URL = "/api/events/"


def iso(value):
    # Same format DRF uses for UTC datetimes in responses.
    return value.isoformat().replace("+00:00", "Z")


class EventApiTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.organization = Organization.objects.create(name="Klub Močvara")
        self.organizer = self.make_organizer("Marko Marić", "marko@gmail.com")
        self.other_organizer = self.make_organizer("Ana Anić", "ana@gmail.com")
        self.user = User.objects.create_user(username="Iva Ivić", email="iva@gmail.com", password=None)

        # Created by the data migration.
        self.music = Category.objects.get(category_name="music")
        self.theatre = Category.objects.get(category_name="theatre")

        self.start = timezone.now().replace(microsecond=0) + timedelta(days=30)
        self.end = self.start + timedelta(hours=3)

    def make_organizer(self, username, email):
        return User.objects.create_user(
            username=username,
            email=email,
            password=None,
            role=Role.get(Role.ORGANIZER),
            organization=self.organization,
        )

    def payload(self, **changes):
        data = {
            "event_name": "Koncert",
            "event_description": "Opis koncerta",
            "category_ids": [self.music.pk],
            "start": iso(self.start),
            "end": iso(self.end),
            "location": "Močvara, Trnjanski nasip bb, Zagreb",
            "latitude": 45.7905,
            "longitude": 15.9781,
            "entry_price": "10.00",
            "price_currency": "EUR",
        }
        data.update(changes)
        return {key: value for key, value in data.items() if value is not ...}

    def post(self, data, client=None):
        return (client or self.client).post(EVENTS_URL, data, content_type="application/json")

    def patch(self, event, data):
        return self.client.patch(f"{EVENTS_URL}{event.pk}/", data, content_type="application/json")

    def delete(self, event):
        return self.client.delete(f"{EVENTS_URL}{event.pk}/")

    def make_event(self, organizer=None, **fields):
        fields.setdefault("event_name", "Koncert")
        fields.setdefault("start", self.start)
        fields.setdefault("end", self.end)
        fields.setdefault("location", "Močvara")
        event = Event.objects.create(organizer=organizer, **fields)
        event.categories.add(self.music)
        return event


class PublishEventTests(EventApiTestCase):
    """F-010: an organizer can add their own events."""

    def test_organizer_publishes_event(self):
        self.client.force_login(self.organizer)
        resp = self.post(self.payload())

        self.assertEqual(resp.status_code, 201)
        event = Event.objects.get()
        self.assertEqual(event.organizer, self.organizer)
        self.assertEqual(
            resp.json(),
            {
                "event_id": event.pk,
                "event_name": "Koncert",
                "event_description": "Opis koncerta",
                "categories": [{"id": self.music.pk, "category_name": "music"}],
                "start": iso(self.start),
                "end": iso(self.end),
                "location": "Močvara, Trnjanski nasip bb, Zagreb",
                "latitude": "45.7905",
                "longitude": "15.9781",
                "entry_price": "10.00",
                "price_currency": "EUR",
                "organizer": {
                    "id": str(self.organizer.pk),
                    "username": "Marko Marić",
                    "organization": "Klub Močvara",
                },
                "is_imported": False,
            },
        )

    def test_start_with_utc_offset_is_accepted(self):
        self.client.force_login(self.organizer)
        local = timezone.get_fixed_timezone(60)
        resp = self.post(self.payload(start=self.start.astimezone(local).isoformat()))

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["start"], iso(self.start))

    def test_only_required_fields(self):
        self.client.force_login(self.organizer)
        resp = self.post(
            self.payload(
                event_description=..., latitude=..., longitude=..., entry_price=..., price_currency=...
            )
        )

        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        for field in ["event_description", "latitude", "longitude", "entry_price", "price_currency"]:
            self.assertIsNone(body[field])

    def test_several_categories(self):
        self.client.force_login(self.organizer)
        resp = self.post(self.payload(category_ids=[self.music.pk, self.theatre.pk]))

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(
            sorted(category["category_name"] for category in resp.json()["categories"]),
            ["music", "theatre"],
        )

    def test_price_without_currency_defaults_to_eur(self):
        self.client.force_login(self.organizer)
        resp = self.post(self.payload(price_currency=...))

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["price_currency"], "EUR")

    def test_organizer_and_ticketmaster_id_cannot_be_set_by_client(self):
        self.client.force_login(self.organizer)
        resp = self.post(self.payload(organizer=str(self.other_organizer.pk), ticketmaster_id="tm-1", event_id=999))

        self.assertEqual(resp.status_code, 201)
        event = Event.objects.get()
        self.assertEqual(event.organizer, self.organizer)
        self.assertIsNone(event.ticketmaster_id)
        self.assertNotEqual(event.pk, 999)

    def test_published_event_is_visible_in_event_list(self):
        self.client.force_login(self.organizer)
        event_id = self.post(self.payload()).json()["event_id"]
        self.client.logout()

        with mock.patch("events.views.sync_events"):
            resp = self.client.get(EVENTS_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual([event["event_id"] for event in resp.json()], [event_id])

    def test_publishing_does_not_call_ticketmaster(self):
        self.client.force_login(self.organizer)
        with mock.patch("events.views.sync_events") as sync:
            self.post(self.payload())
        sync.assert_not_called()

    def test_regular_user_cannot_publish(self):
        self.client.force_login(self.user)
        self.assertEqual(self.post(self.payload()).status_code, 403)
        self.assertFalse(Event.objects.exists())

    def test_anonymous_cannot_publish(self):
        self.assertEqual(self.post(self.payload()).status_code, 403)
        self.assertFalse(Event.objects.exists())

    def test_csrf_token_is_required(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.organizer)
        self.assertEqual(self.post(self.payload(), client=client).status_code, 403)

        client.get("/api/auth/csrf/")
        resp = client.post(
            EVENTS_URL,
            self.payload(),
            content_type="application/json",
            headers={"X-CSRFToken": client.cookies["csrftoken"].value},
        )
        self.assertEqual(resp.status_code, 201)

    def test_required_fields(self):
        self.client.force_login(self.organizer)
        resp = self.post({})

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json(),
            {
                field: ["This field is required."]
                for field in ["event_name", "category_ids", "start", "end", "location"]
            },
        )
        self.assertFalse(Event.objects.exists())

    def test_invalid_data(self):
        self.client.force_login(self.organizer)
        cases = [
            ({"event_name": "  "}, "event_name"),
            ({"location": ""}, "location"),
            ({"category_ids": []}, "category_ids"),
            ({"category_ids": [999999]}, "category_ids"),
            ({"end": iso(self.start)}, "end"),
            ({"end": iso(self.start - timedelta(hours=1))}, "end"),
            ({"start": iso(timezone.now() - timedelta(days=1))}, "start"),
            ({"start": "next friday"}, "start"),
            ({"start": None}, "start"),
            ({"entry_price": "-1.00"}, "entry_price"),
            ({"entry_price": "free"}, "entry_price"),
            ({"latitude": 91}, "latitude"),
            ({"longitude": -181}, "longitude"),
            ({"latitude": "north"}, "latitude"),
            ({"latitude": "nan"}, "latitude"),
            ({"longitude": ...}, "latitude"),
            ({"latitude": None}, "latitude"),
        ]
        for changes, field in cases:
            with self.subTest(changes=changes):
                resp = self.post(self.payload(**changes))
                self.assertEqual(resp.status_code, 400)
                self.assertEqual(list(resp.json()), [field])
        self.assertFalse(Event.objects.exists())


class EditEventTests(EventApiTestCase):
    """F-004: an organizer can edit their own event."""

    def test_owner_edits_single_field(self):
        event = self.make_event(self.organizer, event_description="Stari opis")
        self.client.force_login(self.organizer)
        resp = self.patch(event, {"event_name": "Koncert (novi termin)"})

        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["event_name"], "Koncert (novi termin)")
        self.assertEqual(body["event_description"], "Stari opis")
        self.assertEqual(body["start"], iso(self.start))
        self.assertEqual(body["categories"], [{"id": self.music.pk, "category_name": "music"}])
        event.refresh_from_db()
        self.assertEqual(event.event_name, "Koncert (novi termin)")

    def test_owner_edits_all_fields(self):
        event = self.make_event(self.organizer)
        self.client.force_login(self.organizer)
        new_start = self.start + timedelta(days=1)
        resp = self.patch(
            event,
            self.payload(
                event_name="Predstava",
                category_ids=[self.theatre.pk],
                start=iso(new_start),
                end=iso(new_start + timedelta(hours=2)),
                location="HNK, Zagreb",
                entry_price="15.50",
            ),
        )

        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["event_name"], "Predstava")
        self.assertEqual(body["categories"], [{"id": self.theatre.pk, "category_name": "theatre"}])
        self.assertEqual(body["start"], iso(new_start))
        self.assertEqual(body["location"], "HNK, Zagreb")
        self.assertEqual(body["entry_price"], "15.50")
        self.assertEqual(list(event.categories.all()), [self.theatre])

    def test_changes_are_visible_to_users(self):
        event = self.make_event(self.organizer)
        self.client.force_login(self.organizer)
        self.patch(event, {"event_name": "Novi naziv"})
        self.client.logout()

        self.assertEqual(self.client.get(f"{EVENTS_URL}{event.pk}/").json()["event_name"], "Novi naziv")
        with mock.patch("events.views.sync_events"):
            self.assertEqual(self.client.get(EVENTS_URL).json()[0]["event_name"], "Novi naziv")

    def test_organizer_cannot_be_changed(self):
        event = self.make_event(self.organizer)
        self.client.force_login(self.organizer)
        resp = self.patch(event, {"organizer": str(self.other_organizer.pk), "ticketmaster_id": "tm-1"})

        self.assertEqual(resp.status_code, 200)
        event.refresh_from_db()
        self.assertEqual(event.organizer, self.organizer)
        self.assertIsNone(event.ticketmaster_id)

    def test_invalid_edit(self):
        event = self.make_event(self.organizer, latitude="45.79", longitude="15.97")
        self.client.force_login(self.organizer)
        cases = [
            ({"event_name": ""}, "event_name"),
            ({"location": None}, "location"),
            ({"category_ids": []}, "category_ids"),
            # Compared with the stored start / end.
            ({"end": iso(self.start - timedelta(hours=1))}, "end"),
            ({"start": iso(self.end + timedelta(hours=1))}, "end"),
            ({"start": iso(timezone.now() - timedelta(days=1))}, "start"),
            ({"entry_price": "-5"}, "entry_price"),
            ({"latitude": None}, "latitude"),
            ({"longitude": 200}, "longitude"),
        ]
        for changes, field in cases:
            with self.subTest(changes=changes):
                resp = self.patch(event, changes)
                self.assertEqual(resp.status_code, 400)
                self.assertEqual(list(resp.json()), [field])
        event.refresh_from_db()
        self.assertEqual(event.event_name, "Koncert")
        self.assertEqual(event.start, self.start)

    def test_event_that_already_started_can_still_be_corrected(self):
        started = timezone.now().replace(microsecond=0) - timedelta(hours=1)
        event = self.make_event(self.organizer, start=started, end=started + timedelta(hours=5))
        self.client.force_login(self.organizer)

        # The edit form sends every field back, including the unchanged start.
        resp = self.patch(event, {"event_description": "Vrata se otvaraju u 20h", "start": iso(started)})
        self.assertEqual(resp.status_code, 200)

        resp = self.patch(event, {"start": iso(started - timedelta(hours=1))})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(list(resp.json()), ["start"])

    def test_other_organizer_cannot_edit(self):
        # Even an organizer from the same organization: the event belongs to its author.
        event = self.make_event(self.organizer)
        self.client.force_login(self.other_organizer)
        resp = self.patch(event, {"event_name": "Hakirano"})

        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {"detail": "You can only manage your own events."})
        event.refresh_from_db()
        self.assertEqual(event.event_name, "Koncert")

    def test_user_and_anonymous_cannot_edit(self):
        event = self.make_event(self.organizer)
        self.assertEqual(self.patch(event, {"event_name": "Hakirano"}).status_code, 403)
        self.client.force_login(self.user)
        self.assertEqual(self.patch(event, {"event_name": "Hakirano"}).status_code, 403)
        event.refresh_from_db()
        self.assertEqual(event.event_name, "Koncert")

    def test_imported_event_cannot_be_edited(self):
        event = self.make_event(ticketmaster_id="tm-1")
        self.client.force_login(self.organizer)
        self.assertEqual(self.patch(event, {"event_name": "Hakirano"}).status_code, 403)

    def test_unknown_event(self):
        self.client.force_login(self.organizer)
        resp = self.client.patch(f"{EVENTS_URL}999999/", {"event_name": "x"}, content_type="application/json")
        self.assertEqual(resp.status_code, 404)

    def test_put_is_not_supported(self):
        event = self.make_event(self.organizer)
        self.client.force_login(self.organizer)
        resp = self.client.put(f"{EVENTS_URL}{event.pk}/", self.payload(), content_type="application/json")
        self.assertEqual(resp.status_code, 405)


class DeleteEventTests(EventApiTestCase):
    """F-004: an organizer can delete their own event."""

    def test_owner_deletes_event(self):
        event = self.make_event(self.organizer)
        other_event = self.make_event(self.other_organizer, event_name="Tuđi koncert")
        Comments.objects.create(event=event, user=self.user, time=timezone.now(), rating=5)
        self.client.force_login(self.organizer)

        resp = self.delete(event)

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(list(Event.objects.all()), [other_event])
        self.assertFalse(Comments.objects.exists())
        self.assertFalse(Event_Categories.objects.filter(event_id=event.pk).exists())
        # The category itself and the comment author are untouched.
        self.assertTrue(Category.objects.filter(pk=self.music.pk).exists())
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_deleted_event_is_no_longer_shown(self):
        event = self.make_event(self.organizer)
        self.client.force_login(self.organizer)
        self.delete(event)

        self.assertEqual(self.client.get(f"{EVENTS_URL}{event.pk}/").status_code, 404)
        self.assertEqual(self.client.get(f"{EVENTS_URL}mine/").json(), [])
        with mock.patch("events.views.sync_events"):
            self.assertEqual(self.client.get(EVENTS_URL).json(), [])

    def test_other_organizer_cannot_delete(self):
        event = self.make_event(self.organizer)
        self.client.force_login(self.other_organizer)
        self.assertEqual(self.delete(event).status_code, 403)
        self.assertTrue(Event.objects.filter(pk=event.pk).exists())

    def test_user_and_anonymous_cannot_delete(self):
        event = self.make_event(self.organizer)
        self.assertEqual(self.delete(event).status_code, 403)
        self.client.force_login(self.user)
        self.assertEqual(self.delete(event).status_code, 403)
        self.assertTrue(Event.objects.filter(pk=event.pk).exists())

    def test_imported_event_cannot_be_deleted(self):
        event = self.make_event(ticketmaster_id="tm-1")
        self.client.force_login(self.organizer)
        self.assertEqual(self.delete(event).status_code, 403)
        self.assertTrue(Event.objects.filter(pk=event.pk).exists())


class ReadEventTests(EventApiTestCase):
    def test_event_detail_is_public(self):
        event = self.make_event(self.organizer)
        resp = self.client.get(f"{EVENTS_URL}{event.pk}/")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["organizer"]["organization"], "Klub Močvara")
        self.assertIs(resp.json()["is_imported"], False)

    def test_imported_event_detail(self):
        event = self.make_event(ticketmaster_id="tm-1", start=None, end=None, location=None)
        body = self.client.get(f"{EVENTS_URL}{event.pk}/").json()

        self.assertIsNone(body["organizer"])
        self.assertIsNone(body["start"])
        self.assertIs(body["is_imported"], True)

    def test_my_events_lists_only_own_events(self):
        mine = self.make_event(self.organizer)
        self.make_event(self.other_organizer, event_name="Tuđi koncert")
        self.make_event(ticketmaster_id="tm-1")
        self.client.force_login(self.organizer)

        resp = self.client.get(f"{EVENTS_URL}mine/")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual([event["event_id"] for event in resp.json()], [mine.pk])

    def test_my_events_is_for_organizers_only(self):
        self.assertEqual(self.client.get(f"{EVENTS_URL}mine/").status_code, 403)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(f"{EVENTS_URL}mine/").status_code, 403)

    def test_categories(self):
        resp = self.client.get("/api/categories/")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            [category["category_name"] for category in resp.json()],
            ["education", "festivals", "music", "sport", "theatre"],
        )
        self.assertEqual(set(resp.json()[0]), {"id", "category_name"})

class EventSearchTests(TestCase):
    """F-008: events can be searched by event name or organizer's organization name."""

    @classmethod
    def setUpTestData(cls):
        organization = Organization.objects.create(name="Lisinski")
        organizer = User.objects.create_user(
            "marko",
            "marko@example.com",
            role=Role.get(Role.ORGANIZER),
            organization=organization,
        )
        Event.objects.create(
            event_name="Jazz večer",
            organizer=organizer,
            start=datetime(2026, 12, 1, 20, 0, tzinfo=timezone.utc),
        )
        Event.objects.create(
            event_name="Simfonijski koncert",
            organizer=organizer,
            start=datetime(2026, 12, 3, 20, 0, tzinfo=timezone.utc),
        )
        # No organizer, like events imported from Ticketmaster
        Event.objects.create(
            event_name="Jazz festival",
            start=datetime(2026, 12, 2, 20, 0, tzinfo=timezone.utc),
        )

    def setUp(self):
        # Never call the real Ticketmaster API from tests
        self.sync_events = mock.patch("events.views.sync_events").start()
        self.addCleanup(mock.patch.stopall)

    def get_event_names(self, **params):
        response = self.client.get(reverse("get_events"), params)
        self.assertEqual(response.status_code, 200)
        return [event["event_name"] for event in response.json()]

    def test_without_search_returns_all_events_ordered_by_start(self):
        self.assertEqual(
            self.get_event_names(),
            ["Jazz večer", "Jazz festival", "Simfonijski koncert"],
        )

    def test_search_by_event_name_is_case_insensitive(self):
        self.assertEqual(self.get_event_names(search="JAZZ"), ["Jazz večer", "Jazz festival"])

    def test_search_by_organization_name(self):
        self.assertEqual(
            self.get_event_names(search="lisinski"),
            ["Jazz večer", "Simfonijski koncert"],
        )

    def test_search_matches_part_of_organization_name(self):
        self.assertEqual(
            self.get_event_names(search="lisin"),
            ["Jazz večer", "Simfonijski koncert"],
        )

    def test_search_does_not_match_organizer_username(self):
        self.assertEqual(self.get_event_names(search="marko"), [])

    def test_all_search_terms_must_match(self):
        self.assertEqual(self.get_event_names(search="jazz lisinski"), ["Jazz večer"])

    def test_event_without_organizer_is_found_by_name(self):
        self.assertEqual(self.get_event_names(search="festival"), ["Jazz festival"])

    def test_search_without_matches_returns_empty_list(self):
        self.assertEqual(self.get_event_names(search="balet"), [])

    def test_ticketmaster_error_returns_502(self):
        self.sync_events.side_effect = httpx.HTTPError("Ticketmaster down")

        response = self.client.get(reverse("get_events"))

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json(), {"error": "Ticketmaster API error"})
