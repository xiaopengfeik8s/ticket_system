# tickets/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('create/', views.ticket_create, name='ticket_create'),
    path('<int:pk>/edit/', views.ticket_edit, name='ticket_edit'),
    path('<int:pk>/delete/', views.ticket_delete, name='ticket_delete'),
    path('<int:pk>/update/<str:status>/', views.ticket_status_update, name='ticket_status_update'),
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),  
    path('<int:pk>/archive/', views.ticket_archive, name='ticket_archive'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ticket/<int:pk>/comment/', views.ticket_comment, name='ticket_comment'),
]