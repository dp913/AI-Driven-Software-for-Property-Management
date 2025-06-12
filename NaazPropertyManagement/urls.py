"""
URL configuration for NaazPropertyManagement project.

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
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from users.views import dashboard_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password reset
    path('', RedirectView.as_view(url='/accounts/login/')),  # Redirect root to login
    path('users/', include('users.urls')),
    path('properties/', include('properties.urls')),
    # path('maintenance/', include('maintenance.urls')),
    # path('payments/', include('payments.urls')),
    # path('messages/', include('messaging.urls')),
    # path('compliance/', include('compliance.urls')),
    path('dashboard/', dashboard_redirect, name='dashboard'),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)