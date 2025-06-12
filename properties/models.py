from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
import os
import re

# Create your models here.
# class Landlord(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

def property_image_upload_path(instance, filename):
    # Remove special characters and spaces, make it safe for file system
    safe_address = re.sub(r'[^a-zA-Z0-9_-]', '', instance.property.address[:20])
    return f'property_photos/{instance.property.id}_{safe_address}/{filename}'

class Property(models.Model):
    landlord = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'landlord'})
    # name = models.CharField(max_length=100)
    address = models.TextField()
    # photo = models.ImageField(upload_to='property_photos/', blank=True, null=True)
    unit_count = models.IntegerField(default=1)
    managed_by = models.ForeignKey(  # NEW FIELD
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_properties',
        limit_choices_to={'role': 'manager'}
    )
    # You can also add a property manager field if needed

    def __str__(self):
        return self.address

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=property_image_upload_path)

    def __str__(self):
        return f"Image for {self.property.address}"


class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=10)
    tenant = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'tenant'})
    rent_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    lease_start = models.DateField(null=True, blank=True)
    lease_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Unit {self.unit_number} - {self.property.address}"
