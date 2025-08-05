from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list_view, name='event_list'),
    path('create/', views.event_create_view, name='event_create'),
    path('<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('<int:event_id>/attend-toggle/', views.event_attend_toggle_view, name='event_attend_toggle'),
]