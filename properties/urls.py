from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager_properties, name='manager_properties'),
    path('add/', views.add_property, name='add_property'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('<int:pk>/add-tenant/', views.add_tenant_to_property, name='add_tenant_to_property'),
    path('<int:property_id>/units/', views.edit_units, name='edit_units'),
    path('delete/<int:pk>/', views.delete_property, name='delete_property'),
    path('unit/<int:unit_id>/remove-tenant/', views.remove_tenant, name='remove_tenant'),
    path('landlord/properties/', views.landlord_property_list, name='landlord_property_list'),
    path('landlord/properties/<int:property_id>/', views.landlord_property_detail, name='landlord_property_detail'),
    path('landlord/unit/<int:unit_id>/', views.landlord_unit_detail, name='landlord_unit_detail'),

]