from django.urls import path
from . import views

urlpatterns = [
    path('tenant/', views.tenant_dashboard, name='tenant-dashboard'),
    path('landlord/', views.landlord_dashboard, name='landlord-dashboard'),
    path('manager/', views.manager_dashboard, name='manager-dashboard'),
]