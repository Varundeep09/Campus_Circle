from django.urls import path
from . import views
from .notifications import get_notifications

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('verify_alumni/<int:user_id>/', views.verify_alumni_view, name='verify_alumni'),
    path('dashboard/student/', views.dashboard_student, name='dashboard_student'),
    path('dashboard/teacher/', views.dashboard_teacher, name='dashboard_teacher'),
    path('dashboard/alumni/', views.dashboard_alumni, name='dashboard_alumni'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    # Alumni verification
    path('alumni/request-verification/', views.request_alumni_verification, name='request_alumni_verification'),
    path('admin/alumni-verifications/', views.manage_alumni_verifications, name='manage_alumni_verifications'),
    path('admin/alumni-verifications/<int:req_id>/<str:action>/', views.process_alumni_verification, name='process_alumni_verification'),
    path('api/notifications/', get_notifications, name='get_notifications'),
]