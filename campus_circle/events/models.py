from django.conf import settings
from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='organized_events')
    location = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attending_events', blank=True)

    def __str__(self):
        return self.title