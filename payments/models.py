from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# class Payment(models.Model):
#     tenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tenant'})
#     unit = models.ForeignKey('properties.Unit', on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=8, decimal_places=2)
#     due_date = models.DateField()
#     paid = models.BooleanField(default=False)
#     paid_on = models.DateTimeField(null=True, blank=True)
#     receipt = models.FileField(upload_to='receipts/', blank=True)
#     stripe_payment_id = models.CharField(max_length=100, blank=True)