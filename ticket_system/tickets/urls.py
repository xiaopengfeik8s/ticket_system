# tickets/urls.py
from django.urls import path
from .views import ticket_list, ticket_create, ticket_edit, ticket_delete
from . import views

urlpatterns = [
    path('', ticket_list, name='ticket_list'),
    path('create/', ticket_create, name='ticket_create'),
    path('<int:pk>/edit/', ticket_edit, name='ticket_edit'),
    path('<int:pk>/delete/', ticket_delete, name='ticket_delete'),
    path('<int:pk>/update/<str:status>/', views.ticket_status_update, name='ticket_status_update'),
]