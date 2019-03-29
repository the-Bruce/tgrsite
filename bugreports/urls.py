from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(template_name='bugreports/index.html'), name='bug_index'),
    path('<int:pk>/', views.Detail.as_view(), name='bug_detail'),
    path('create/', views.Create.as_view(), name='bug_create'),
]
