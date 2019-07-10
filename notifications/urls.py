from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    path('', views.all_notifications, name='all_notifications'),
    path('clear/', views.read_all, name='clear_notifications'),
    path('read/<int:pk>/', views.mark_read, name='read_notification'),
    path('preferences/', views.UpdateSubscriptions.as_view(), name='notification_settings'),
    path('temp/', views.email_notifications)
]
