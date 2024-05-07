# tickets/urls.py
from django.urls import path
from .views import ticket_list, ticket_create

urlpatterns = [
    path('', ticket_list, name='ticket_list'),
    path('create/', ticket_create, name='ticket_create'),
]