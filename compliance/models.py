from django.db import models

# Create your models here.
# class ComplianceChecklist(models.Model):
#     property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
#     item = models.CharField(max_length=255)
#     due_date = models.DateField()
#     is_completed = models.BooleanField(default=False)
#     proof = models.FileField(upload_to='compliance_docs/', blank=True)
#     created_by_ai = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)