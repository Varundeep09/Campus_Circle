from django import forms
from .models import Event
from django.forms.widgets import DateTimeInput

class EventForm(forms.ModelForm):
    event_date = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_date']