from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class MaintenanceRequest(models.Model):
#     STATUS_CHOICES = [
#         ('requested', 'Requested'),
#         ('in_progress', 'In Progress'),
#         ('resolved', 'Resolved'),
#     ]
#     PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
#
#     tenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tenant'})
#     unit = models.ForeignKey('properties.Unit', on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     photo = models.ImageField(upload_to='maintenance_photos/', blank=True)
#     priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
#     assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_maintenance')
#     created_at = models.DateTimeField(auto_now_add=True)