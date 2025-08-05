from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),               # List all message threads
    path('thread/<int:thread_id>/', views.thread_detail_view, name='thread'),  # View specific thread/conversation
    path('thread/new/', views.new_thread_view, name='new_thread'),  # Create new conversation
]