from django.urls import path

from . import views

urlpatterns = [
    path('', views.page, {'name': 'index'}, name='homepage'),
    path('schedule/', views.page, {'name': 'schedule'}, name='schedule'),
    path('sponsorships/', views.page, {'name': 'sponsorships'}, name='sponsorships'),
    path('larp/', views.page, {'name':'larp_main'}, name='larp_info'),
    path('larp/lore/', views.page, {'name':'larp_main'}, name='larp_lore'),
    path('page/<name>/', views.page, name='page'),
]
