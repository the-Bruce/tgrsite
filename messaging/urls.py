from django.urls import path

from . import views

app_name = "message"
urlpatterns = [
    path('', views.index, name='message_list'),

    # DEPRECATED
    # url(r'^dm$', views.dm, name='message_dm'),

    path('direct_message/', views.direct_message, name='message_direct'),
    path('group_message/<int:threadid>/', views.group_message, name='message_group'),

    path('thread/<int:pk>/', views.thread, name='message_thread'),
    path('thread/name/', views.rename_thread, name='rename_thread'),
    path('dm_thread/<int:recipient>/', views.get_dm_thread, name='get_dm_thread'),
]
