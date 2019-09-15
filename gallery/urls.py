from django.urls import path

from . import views

app_name = "gallery"

urlpatterns = [
    path('', views.Index.as_view(), name='gallery'),
]
