from django.urls import path

from . import views

app_name = "exec"
urlpatterns = [
    path('', views.Index.as_view(), name='exec'),
    path('editbio/<int:pk>/', views.Edit.as_view(), name='exec_editbio'),
]
