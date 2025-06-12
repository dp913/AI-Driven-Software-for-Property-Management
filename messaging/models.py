from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# class MessageThread(models.Model):
#     participants = models.ManyToManyField(User)
#     property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, null=True, blank=True)
#
# class Message(models.Model):
#     thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     body = models.TextField()
#     sent_at = models.DateTimeField(auto_now_add=True)