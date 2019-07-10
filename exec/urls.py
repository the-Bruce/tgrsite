from django.urls import path

from . import views

app_name="exec"
urlpatterns = [
    path('', views.index, name='exec'),
    path('editbio/<int:pk>/', views.editbio, name='exec_editbio'),
    path('editbio/<int:pk>/done/', views.editbio_done, name='exec_editbio_done'),
]
