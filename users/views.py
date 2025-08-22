
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User
from .forms import CustomUserCreationForm, ProfileForm, AlumniVerificationRequestForm
from .models import AlumniVerificationRequest
from django.utils import timezone

# Alumni: Request verification
@login_required
def request_alumni_verification(request):
    if request.user.role != User.ALUMNI:
        messages.error(request, "Only alumni can request verification.")
        return redirect('users:dashboard_alumni')
    existing = AlumniVerificationRequest.objects.filter(user=request.user, status='pending').first()
    if existing:
        messages.info(request, "You already have a pending verification request.")
        return redirect('users:dashboard_alumni')
    if request.method == 'POST':
        form = AlumniVerificationRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.user = request.user
            req.save()
            messages.success(request, "Verification request submitted to admin.")
            return redirect('users:dashboard_alumni')
    else:
        form = AlumniVerificationRequestForm()
    return render(request, 'users/request_alumni_verification.html', {'form': form})

# Admin: Approve/Deny alumni requests
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def manage_alumni_verifications(request):
    requests = AlumniVerificationRequest.objects.filter(status='pending').select_related('user')
    return render(request, 'users/manage_alumni_verifications.html', {'requests': requests})

@staff_member_required
def process_alumni_verification(request, req_id, action):
    req = get_object_or_404(AlumniVerificationRequest, id=req_id, status='pending')
    if action == 'approve':
        req.status = 'approved'
        req.reviewed_at = timezone.now()
        req.reviewed_by = request.user
        req.user.is_alumni_verified = True
        req.user.save()
        req.save()
        messages.success(request, f"Approved alumni verification for {req.user.username}.")
    elif action == 'deny':
        req.status = 'denied'
        req.reviewed_at = timezone.now()
        req.reviewed_by = request.user
        req.save()
        messages.info(request, f"Denied alumni verification for {req.user.username}.")
    return redirect('users:manage_alumni_verifications')
from .utils import role_required
from .notifications import get_notifications


# Dashboard views for each role

from social.models import Post
from jobs.models import JobPosting
from events.models import Event
from django.utils import timezone

@login_required
def dashboard_student(request):
    posts = Post.objects.all().order_by('-created_at')[:5]
    jobs = JobPosting.objects.all().order_by('-created_at')[:5]
    events = Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')[:5]
    return render(request, 'users/dashboard_student.html', {
        'posts': posts,
        'jobs': jobs,
        'events': events,
    })

@login_required
def dashboard_teacher(request):
    # Events organized by this teacher
    events = Event.objects.filter(organizer=request.user).order_by('-event_date')[:5]
    posts = Post.objects.all().order_by('-created_at')[:5]
    return render(request, 'users/dashboard_teacher.html', {
        'events': events,
        'posts': posts,
    })

@login_required
def dashboard_alumni(request):
    # Jobs posted by alumni, verification status, and latest posts
    jobs = JobPosting.objects.filter(posted_by=request.user).order_by('-created_at')[:5]
    posts = Post.objects.all().order_by('-created_at')[:5]
    alumni_verified = getattr(request.user, 'is_alumni_verified', False)
    pending_request = None
    if not alumni_verified:
        pending_request = AlumniVerificationRequest.objects.filter(user=request.user, status='pending').first()
    return render(request, 'users/dashboard_alumni.html', {
        'jobs': jobs,
        'posts': posts,
        'alumni_verified': alumni_verified,
        'pending_request': pending_request,
    })

@login_required
def dashboard_admin(request):
    # List all users and latest posts for moderation
    all_users = User.objects.all().order_by('-date_joined')[:10]
    posts = Post.objects.all().order_by('-created_at')[:10]
    jobs = JobPosting.objects.all().order_by('-created_at')[:5]
    events = Event.objects.all().order_by('-event_date')[:5]
    return render(request, 'users/dashboard_admin.html', {
        'all_users': all_users,
        'posts': posts,
        'jobs': jobs,
        'events': events,
        'show_admin_controls': True,
    })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('social:feed')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('social:feed')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        selected_role = request.POST.get('role', '').strip()
        
        if not username or not password or not selected_role:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'users/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user and user.is_active:
            # Handle superuser case
            if user.is_superuser:
                if user.role != 'admin':
                    user.role = 'admin'
                    user.save()
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                return redirect('users:dashboard_admin')
            
            # Check if selected role matches user's actual role
            if user.role == selected_role:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                
                # Redirect based on role
                if user.role == 'student':
                    return redirect('users:dashboard_student')
                elif user.role == 'teacher':
                    return redirect('users:dashboard_teacher')
                elif user.role == 'alumni':
                    return redirect('users:dashboard_alumni')
                elif user.role == 'admin':
                    return redirect('users:dashboard_admin')
                else:
                    return redirect('social:feed')
            else:
                messages.error(request, f"Role mismatch! Your account is registered as '{user.get_role_display()}', but you selected '{selected_role.title()}'.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('users:login')

@login_required
def profile_view(request, username=None):
    if username:
        user_profile = get_object_or_404(User, username=username)
    else:
        user_profile = request.user

    return render(request, 'users/profile.html', {'profile_user': user_profile})

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('users:profile', username=request.user.username)
        else:
            messages.error(request, "Please correct errors below.")
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})

# Admin-only alumni verification view (for example)
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def verify_alumni_view(request, user_id):
    user_obj = get_object_or_404(User, id=user_id, role=User.ALUMNI)
    if request.method == 'POST':
        user_obj.is_alumni_verified = True
        user_obj.save()
        messages.success(request, f"{user_obj.username} is now verified as alumni.")
        return redirect('admin:index')
    return render(request, 'users/verify_alumni.html', {'user_obj': user_obj})