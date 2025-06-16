from django.urls import path
from . import views

urlpatterns = [
    path('tenant/', views.tenant_dashboard, name='tenant-dashboard'),
    path('unit/<int:unit_id>/', views.tenant_unit_detail, name='tenant_unit_detail'),
    path('landlord/', views.landlord_dashboard, name='landlord-dashboard'),
    path('manager/', views.manager_dashboard, name='manager-dashboard'),
]