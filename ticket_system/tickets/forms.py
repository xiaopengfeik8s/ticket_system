from django import forms
from .models import Ticket,Comment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'labels', 'assigned_to']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)