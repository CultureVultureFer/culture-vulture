from django.urls import path
from events import views

urlpatterns = [
    path("events/", views.EventListView.as_view(), name="get_events"),
    path("events/mine/", views.my_events_view, name="my-events"),
    path("categories/", views.categories_view, name="categories"),
    path("events/<int:event_id>/", views.event_detail_view, name="event-detail"),
]
