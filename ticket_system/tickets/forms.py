from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'labels']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)