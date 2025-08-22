from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobPosting, JobApplication
from .forms import JobPostingForm
from users.utils import role_required
from django.utils import timezone
from django.utils.html import escape
from django.db import IntegrityError
import os

@login_required
def job_list_view(request):
    jobs = JobPosting.objects.filter(application_deadline__gte=timezone.now().date())
    search = request.GET.get('search', '').strip()
    location = request.GET.get('location', '').strip()
    if search:
        jobs = jobs.filter(title__icontains=search) | jobs.filter(company__icontains=search)
    if location:
        jobs = jobs.filter(location__iexact=location)
    jobs = jobs.order_by('-created_at')
    # For filter dropdown
    locations = JobPosting.objects.values_list('location', flat=True).distinct()
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'locations': locations})

@login_required
def job_detail_view(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
@role_required('alumni', 'teacher', 'admin')  # allow alumni verified, teacher, admin to post jobs
def job_post_create_view(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.posted_by = request.user
            job_post.save()
            messages.success(request, "Job posted successfully.")
            return redirect('jobs:job_detail', job_id=job_post.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobPostingForm()
    return render(request, 'jobs/job_post_create.html', {'form': form})

@login_required
@role_required('alumni', 'teacher', 'admin')
def job_post_edit_view(request, job_id):
    job_post = get_object_or_404(JobPosting, id=job_id, posted_by=request.user)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect('jobs:job_detail', job_id=job_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobPostingForm(instance=job_post)
    return render(request, 'jobs/job_post_edit.html', {'form': form, 'job_post': job_post})

@login_required
@role_required('alumni', 'teacher', 'admin')
def job_post_delete_view(request, job_id):
    job_post = get_object_or_404(JobPosting, id=job_id, posted_by=request.user)
    if request.method == "POST":
        job_post.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('jobs:job_list')
    return render(request, 'jobs/job_post_delete_confirm.html', {'job_post': job_post})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    
    # Check if user is a student
    if request.user.role != 'student':
        messages.error(request, "Only students can apply for jobs.")
        return redirect('jobs:job_detail', job_id=job_id)
    
    # Check if application deadline has passed
    if job.application_deadline < timezone.now().date():
        messages.error(request, "Application deadline has passed.")
        return redirect('jobs:job_detail', job_id=job_id)
    
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '').strip()
        
        if not cover_letter:
            messages.error(request, "Cover letter is required.")
            return redirect('jobs:job_detail', job_id=job_id)
        
        try:
            # Create job application
            JobApplication.objects.create(
                job=job,
                applicant=request.user,
                cover_letter=cover_letter
            )
            messages.success(request, f"Your application for {job.title} has been submitted successfully!")
        except IntegrityError:
            messages.error(request, "You have already applied for this job.")
    
    return redirect('jobs:job_detail', job_id=job_id)