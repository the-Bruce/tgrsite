from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_notifications, name='all_notifications'),
    path('clear/', views.read_all, name='clear_notifications'),
    path('read/<int:pk>/', views.mark_read, name='read_notification')
]
