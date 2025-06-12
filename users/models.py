from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
        ('manager', 'Property Manager'),
    )
    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES,
                            default='tenant',
                            help_text="Designates the role of the user in the system."
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"