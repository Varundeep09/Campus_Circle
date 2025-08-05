from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like-toggle/', views.post_like_toggle, name='post_like_toggle'),
]