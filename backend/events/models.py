from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    def __str__(self):
        return self.category_name

class Event(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    ticketmaster_id = models.CharField(max_length=100,
                                        null=True,
                                        unique=True
                                        )
    event_name = models.CharField(max_length=250)
    event_description = models.CharField(null=True, max_length=2000, blank=True)
    organizer = models.ForeignKey("accounts.User", on_delete=models.RESTRICT, null = True, blank = True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    latitude = models.CharField(null=True, blank=True, max_length=50)
    longitude = models.CharField(null=True, blank=True, max_length=50)
    entry_price = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
    price_currency = models.CharField(null=True, blank=True, max_length=30)

    categories = models.ManyToManyField(
        Category,
        through="Event_Categories",
        related_name="events"
    )

    def __str__(self):
        return self.event_name
class UpdateTracker(models.Model):
    next_update = models.DurationField()
    update_frequency = models.TimeField()
    event_lower_bound = models.TimeField()
    event_upper_bound = models.TimeField()
    def __str__(self):
        return f"Next update at {self.next_update}, frequency of {self.update_frequency}"

class Comments(models.Model):
    event = models.ForeignKey(Event, on_delete=models.RESTRICT)
    user = models.ForeignKey("accounts.User", on_delete=models.RESTRICT)
    time = models.DateTimeField()
    rating = models.IntegerField()
    comment_text = models.CharField(max_length=2000, null=True, blank=True)
    def __str__(self):
        return f"Comment by {self.user} on {self.event}"  
class Event_Categories(models.Model):
    event = models.ForeignKey(Event, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    def __str__(self):
        return f"Event {self.event} with Category {self.category}"
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "category"]
                ,name = "unique_event_category"
            )
        ]