from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('post/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('post/create/', views.job_post_create_view, name='job_post_create'),
    path('post/<int:job_id>/edit/', views.job_post_edit_view, name='job_post_edit'),
    path('post/<int:job_id>/delete/', views.job_post_delete_view, name='job_post_delete'),
    path('post/<int:job_id>/apply/', views.apply_job, name='apply_job'),
]