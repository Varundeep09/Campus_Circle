from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from users.models import User
from .models import MessageThread, Message
from .forms import NewThreadForm

@login_required
def inbox_view(request):
    threads = MessageThread.objects.filter(participants=request.user).order_by('-created_at')
    # Attach last_message to each thread for template use
    for thread in threads:
        last_msg = thread.messages.order_by('-created_at').first()
        thread.last_message = last_msg
    return render(request, 'messaging/inbox.html', {'threads': threads})

@login_required
def thread_detail_view(request, thread_id):
    thread = get_object_or_404(MessageThread, id=thread_id)
    if request.user not in thread.participants.all():
        messages.error(request, "You do not have permission to view this conversation.")
        return redirect('messaging:inbox')

    messages_qs = thread.messages.order_by('created_at')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(thread=thread, sender=request.user, content=content)
            return redirect('messaging:thread', thread_id=thread.id)
        else:
            messages.error(request, "Message content cannot be empty.")

    return render(request, 'messaging/thread.html', {'thread': thread, 'messages': messages_qs})

@login_required
def search_users(request):
    query = request.GET.get('q', '').strip()
    if len(query) >= 2:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).exclude(id=request.user.id)[:10]
        
        results = []
        for user in users:
            avatar_url = '/static/img/default_avatar.svg'
            if hasattr(user, 'profile') and user.profile.profile_image:
                avatar_url = user.profile.profile_image.url
            
            results.append({
                'id': user.id,
                'username': user.username,
                'full_name': user.get_full_name() or user.username,
                'role': user.get_role_display(),
                'avatar': avatar_url
            })
        
        return JsonResponse({'users': results})
    return JsonResponse({'users': []})

@login_required
def new_thread_view(request):
    if request.method == 'POST':
        recipients_input = request.POST.get('recipients', '').strip()
        content = request.POST.get('content', '').strip()
        
        if not recipients_input or not content:
            messages.error(request, "Please select recipients and enter a message.")
            return render(request, 'messaging/new_thread.html')
        
        recipients_usernames = [u.strip() for u in recipients_input.split(',') if u.strip()]
        recipients = User.objects.filter(username__in=recipients_usernames).distinct()
        
        if not recipients.exists():
            messages.error(request, "No valid recipients found.")
            return render(request, 'messaging/new_thread.html')

        if request.user in recipients:
            recipients = recipients.exclude(id=request.user.id)

        if not recipients.exists():
            messages.error(request, "Cannot start conversation with yourself only.")
            return render(request, 'messaging/new_thread.html')

        # Check for existing thread with exact participants
        participants_set = set(list(recipients) + [request.user])
        existing_threads = MessageThread.objects.filter(participants=request.user)
        for thread in existing_threads:
            thread_participants = set(thread.participants.all())
            if thread_participants == participants_set:
                messages.info(request, "Thread already exists, redirecting.")
                return redirect('messaging:thread', thread_id=thread.id)

        # Create new thread
        thread = MessageThread.objects.create()
        thread.participants.add(*recipients)
        thread.participants.add(request.user)

        # Create first message
        Message.objects.create(thread=thread, sender=request.user, content=content)
        messages.success(request, "Conversation started successfully!")
        return redirect('messaging:thread', thread_id=thread.id)
    
    return render(request, 'messaging/new_thread.html')