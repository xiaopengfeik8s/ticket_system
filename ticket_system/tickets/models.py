from django.db import models

# Create your models here.

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
    
    LABEL_CHOICES = [
        ('bug', 'Bug'),
        ('feature_request', 'Feature Request'),
        ('documentation', 'Documentation'),
        ('duplicate', 'Duplicate'),
        ('invalid', 'Invalid'),
    ]
    
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')
    labels = models.CharField(max_length=20, choices=LABEL_CHOICES, default='bug')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)