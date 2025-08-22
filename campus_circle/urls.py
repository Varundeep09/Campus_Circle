"""
URL configuration for campus_circle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from social.views import home_view


def redirect_to_feed(request):
    return redirect('social:feed')

urlpatterns = [
    path('', home_view, name='home'),
    path('', home_view, name='home'),  
    path('', redirect_to_feed, name='home'),   # root URL now redirects to social feed
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('social/', include(('social.urls', 'social'), namespace='social')),
    path('messaging/', include(('messaging.urls', 'messaging'), namespace='messaging')),
    path('events/', include(('events.urls', 'events'), namespace='events')),
    path('jobs/', include(('jobs.urls', 'jobs'), namespace='jobs')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)