from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='rpgs'),
    path('<int:pk>/', views.Detail.as_view(), name='rpg'),
    path('tagged/<slug:tag>/', views.Filter.as_view(), name='rpg_tag'),
    path('tag_form/', views.tag_form, name='rpg_tag_form'),
    path('join/', views.join, name='rpg_join'),

    path('leave/', views.leave, name='rpg_leave'),
    path('kick/', views.kick, name='rpg_kick'),

    path('create/', views.create, name='rpg_create'),
    path('add_to/', views.add_to, name='rpg_add_to'),
    path('<int:pk>/edit/', views.edit, name='rpg_edit'),
    path('<int:pk>/edit/done/', views.edit_process, name='rpg_edit_done'),

    # these are nowhere near usable
    # url(r'^(?P<pk>[0-9]+)/manage$', views.manage, name='rpg_manage'),
    # url(r'^(?P<pk>[0-9]+)/manage/done$', views.manage_process, name='rpg_manage_done'),

    path('<int:pk>/delete/', views.delete, name='rpg_delete'),
    path('create/finish/', views.create_done, name='create_done'),
]
