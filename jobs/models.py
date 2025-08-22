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
    application_link = models.URLField(blank=True, help_text='Link where students will be redirected to apply')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"