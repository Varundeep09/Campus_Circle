from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from jobs.models import JobPosting
from events.models import Event
from messaging.models import Message
from django.utils import timezone
from datetime import timedelta

@login_required
def get_notifications(request):
    notifications = []
    
    # Recent job postings (last 24 hours)
    recent_jobs = JobPosting.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('-created_at')[:5]
    
    for job in recent_jobs:
        notifications.append({
            'title': 'New Job Posted',
            'message': f'{job.title} at {job.company}',
            'time': f'{(timezone.now() - job.created_at).seconds // 3600} hours ago',
            'icon': 'fas fa-briefcase'
        })
    
    # Recent events
    recent_events = Event.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('-created_at')[:3]
    
    for event in recent_events:
        notifications.append({
            'title': 'New Event',
            'message': f'{event.title} on {event.event_date.strftime("%b %d")}',
            'time': f'{(timezone.now() - event.created_at).seconds // 3600} hours ago',
            'icon': 'fas fa-calendar'
        })
    
    # Recent messages for current user
    recent_messages = Message.objects.filter(
        thread__participants=request.user,
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).exclude(sender=request.user).order_by('-created_at')[:3]
    
    for message in recent_messages:
        notifications.append({
            'title': 'New Message',
            'message': f'From {message.sender.get_full_name() or message.sender.username}',
            'time': f'{(timezone.now() - message.created_at).seconds // 3600} hours ago',
            'icon': 'fas fa-envelope'
        })
    
    # Sort by most recent
    notifications = sorted(notifications, key=lambda x: x['time'])[:10]
    
    return JsonResponse({'notifications': notifications})