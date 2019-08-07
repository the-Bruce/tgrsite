from django.urls import path

from . import views

app_name = "forum"

urlpatterns = [
    path('', views.RootForum.as_view(), name='forum'),
    path('<int:forum>/', views.ViewSubforum.as_view(), name='subforum'),

    path('thread/<int:thread>/', views.ViewThread.as_view(), name='viewthread'),

    path('thread/<int:pk>/delete/', views.DeleteThread.as_view(), name='thread_delete'),

    path('thread/<int:pk>/edit/', views.edit_thread_view, name='thread_edit'),

    path('thread/edit/done/', views.edit_thread_process, name='thread_edit_done'),

    path('response/<int:pk>/delete/', views.DeleteResponse.as_view(), name='response_delete'),

    path('response/<int:pk>/edit/', views.EditResponse.as_view(), name='response_edit'),

    path('response/edit/done/', views.edit_response_process, name='response_edit_done'),

]
