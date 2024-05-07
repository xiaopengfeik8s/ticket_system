# tickets/urls.py
from django.urls import path
from .views import ticket_list, ticket_create, ticket_edit, ticket_delete

urlpatterns = [
    path('', ticket_list, name='ticket_list'),
    path('create/', ticket_create, name='ticket_create'),
    path('<int:pk>/edit/', ticket_edit, name='ticket_edit'),
    path('<int:pk>/delete/', ticket_delete, name='ticket_delete'),
]