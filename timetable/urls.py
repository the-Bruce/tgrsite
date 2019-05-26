from django.urls import path

from . import views

urlpatterns = [
    path('', views.TimetableView.as_view(), name='timetable'),
    path('<int:pk>/', views.SingleTimetableView.as_view(), name='single_timetable'),
]
