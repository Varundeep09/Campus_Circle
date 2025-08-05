from django.conf import settings
from django.db import models
from django.utils import timezone

class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='job_postings')
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=100, choices=[('full-time', 'Full-time'), ('part-time', 'Part-time'), ('internship', 'Internship')])
    application_deadline = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} at {self.company}"