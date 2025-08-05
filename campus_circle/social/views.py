from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.http import JsonResponse


@login_required
def home_view(request):
    return render(request, 'social/home.html')

@login_required
def feed(request):
    # Get posts from user and their accepted connections only
    connections = request.user.connections_sent.filter(accepted=True).values_list('to_user_id', flat=True)
    posts = Post.objects.filter(author__in=connections)
    user_posts = Post.objects.filter(author=request.user)
    posts = (posts | user_posts).distinct()
    search = request.GET.get('search', '').strip()
    author = request.GET.get('author', '').strip()
    if search:
        posts = posts.filter(content__icontains=search)
    if author:
        posts = posts.filter(author__username=author)
    posts = posts.order_by('-created_at')
    # For filter dropdown
    authors = Post.objects.values_list('author__username', flat=True).distinct()
    return render(request, 'social/feed.html', {'posts': posts, 'authors': authors})

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
    if request.is_ajax():
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes})
    return redirect('social:feed')