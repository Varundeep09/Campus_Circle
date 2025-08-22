from django.contrib.auth.decorators import login_required
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author and not request.user.is_superuser:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('social:feed')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect('social:feed')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PostForm(instance=post)
    return render(request, 'social/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this post.")
        return redirect('social:feed')
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('social:feed')
    return render(request, 'social/delete_post.html', {'post': post})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.utils.html import escape
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os


@login_required
def home_view(request):
    # Show latest social posts on homepage
    posts = Post.objects.all().order_by('-created_at')[:10]
    return render(request, 'social/home.html', {'posts': posts})

@login_required
def feed(request):
    posts = Post.objects.all()
    search = request.GET.get('search', '').strip()
    author = request.GET.get('author', '').strip()
    if search:
        posts = posts.filter(content__icontains=search)
    if author:
        posts = posts.filter(author__username=author)
    posts = posts.order_by('-created_at')
    authors = Post.objects.values_list('author__username', flat=True).distinct()

    # Handle comment submission
    if request.method == 'POST' and 'comment_post_id' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            post_id = request.POST.get('comment_post_id')
            post = get_object_or_404(Post, id=post_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added.')
            return redirect('social:feed')
    else:
        comment_form = CommentForm()

    return render(request, 'social/feed.html', {'posts': posts, 'authors': authors, 'comment_form': comment_form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('social:feed')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PostForm()
    return render(request, 'social/create_post.html', {'form': form})

@login_required
def post_like_toggle(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes})
    return redirect('social:feed')