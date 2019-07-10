from django.urls import path

from . import views

app_name = "rpgs"

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<int:pk>/', views.Detail.as_view(), name='detail'),
    path('tagged/<str:tag>/', views.Filter.as_view(), name='tag'),
    path('tag_form/', views.tag_form, name='tag_form'),
    path('join/', views.join, name='join'),

    path('leave/', views.leave, name='leave'),
    path('kick/', views.kick, name='kick'),

    path('create/', views.create, name='create'),
    path('add_to/', views.add_to, name='add_to'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/edit/done/', views.edit_process, name='edit_done'),

    # these are nowhere near usable
    # url(r'^(?P<pk>[0-9]+)/manage$', views.manage, name='rpg_manage'),
    # url(r'^(?P<pk>[0-9]+)/manage/done$', views.manage_process, name='rpg_manage_done'),

    path('<int:pk>/delete/', views.delete, name='delete'),
    path('create/finish/', views.create_done, name='create_done'),
]
