from django.urls import path

from . import views

urlpatterns = [
    path('', views.ViewPage.as_view(), {'name': 'index'}, name='homepage'),
    path('page/<slug:name>/', views.ViewPage.as_view(), name='page'),
]
