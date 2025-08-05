from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from users.models import User
from .models import MessageThread, Message
from .forms import NewThreadForm

@login_required
def inbox_view(request):
    threads = MessageThread.objects.filter(participants=request.user).order_by('-created_at')
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
def new_thread_view(request):
    if request.method == 'POST':
        form = NewThreadForm(request.POST)
        if form.is_valid():
            recipients_usernames = [u.strip() for u in form.cleaned_data['recipients'].split(',')]
            recipients = User.objects.filter(username__in=recipients_usernames).distinct()
            if not recipients.exists():
                messages.error(request, "No valid recipients found.")
                return render(request, 'messaging/new_thread.html', {'form': form})

            if request.user in recipients:
                recipients = recipients.exclude(id=request.user.id)

            if not recipients.exists():
                messages.error(request, "Cannot start conversation with yourself only.")
                return render(request, 'messaging/new_thread.html', {'form': form})

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
            thread.participants.add(*participants)
            thread.participants.add(request.user)

            # Create first message
            Message.objects.create(thread=thread, sender=request.user, content=form.cleaned_data['content'])
            return redirect('messaging:thread', thread_id=thread.id)
    else:
        form = NewThreadForm()
    return render(request, 'messaging/new_thread.html', {'form': form})