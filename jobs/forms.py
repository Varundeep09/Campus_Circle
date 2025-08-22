from django import forms
from .models import JobPosting
from django.forms.widgets import DateInput

class JobPostingForm(forms.ModelForm):
    application_deadline = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'company', 'location', 'job_type', 'application_deadline', 'application_link']