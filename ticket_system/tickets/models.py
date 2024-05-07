from django.db import models

# Create your models here.
from django.db import models
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('waiting_for_feedback', 'Waiting for Feedback'),
        ('resolved', 'Resolved'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')
    labels = models.TextField(blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)