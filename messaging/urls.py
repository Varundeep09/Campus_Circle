from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
    path('thread/<int:thread_id>/', views.thread_detail_view, name='thread'),
    path('thread/new/', views.new_thread_view, name='new_thread'),
    path('search-users/', views.search_users, name='search_users'),
]