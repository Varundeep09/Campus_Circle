from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from .forms import EventForm
from users.utils import role_required
from django.utils import timezone

@login_required
def event_list_view(request):
    events = Event.objects.filter(event_date__gte=timezone.now())
    search = request.GET.get('search', '').strip()
    location = request.GET.get('location', '').strip()
    if search:
        events = events.filter(title__icontains=search)
    if location:
        events = events.filter(location__iexact=location)
    events = events.order_by('event_date')
    # For filter dropdown
    locations = Event.objects.values_list('location', flat=True).distinct()
    return render(request, 'events/event_list.html', {'events': events, 'locations': locations})

@login_required
def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_attending = request.user in event.attendees.all()
    return render(request, 'events/event_detail.html', {'event': event, 'is_attending': is_attending})

@login_required
@role_required('teacher', 'admin')
def event_create_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, "Event created successfully.")
            return redirect('events:event_detail', event_id=event.id)
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = EventForm()
    return render(request, 'events/event_create.html', {'form': form})

@login_required
def event_attend_toggle_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    if user in event.attendees.all():
        event.attendees.remove(user)
        messages.info(request, "You have left the event.")
    else:
        event.attendees.add(user)
        messages.success(request, "You are now attending the event.")
    return redirect('events:event_detail', event_id=event.id)