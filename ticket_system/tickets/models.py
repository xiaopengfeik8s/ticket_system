from django.db import models
from django.contrib.auth.models import User
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
    assigned_to = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')
    labels = models.CharField(max_length=20, choices=LABEL_CHOICES, default='bug')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]  # 返回文本的前20个字符
    
    class Meta:
        ordering = ['created_date']  # 根据创建时间排序

    def update_comment(self, new_text):
        self.text = new_text
        self.save()

    def delete_comment(self):
        self.delete()