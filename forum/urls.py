from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='forum'),
    path('<int:pk>/', views.forum, name='subforum'),
    # url(
    #	r'^thread/(?P<pk>[0-9]+)/#response-(?P<response_id>[0-9]+)/$',
    #	views.thread,
    #	name='viewresponse'
    # ),
    path('thread/<int:pk>/', views.thread, name='viewthread'),

    path('thread/respond/', views.create_response, name='createresponse'),

    path('thread/create/', views.create_thread, name='createthread'),

    path('thread/<int:pk>/delete/', views.delete_thread, name='thread_delete'),

    path('thread/<int:pk>/edit/', views.edit_thread_view, name='thread_edit'),

    path('thread/edit/done/', views.edit_thread_process, name='thread_edit_done'),

    path('response/<int:pk>/delete/', views.delete_response, name='response_delete'),

    path('response/<int:pk>/edit/', views.edit_response_view, name='response_edit'),

    path('response/edit/done/', views.edit_response_process, name='response_edit_done'),

]
