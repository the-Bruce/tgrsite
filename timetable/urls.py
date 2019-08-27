from django.urls import path

from . import views

app_name = "timetable"

urlpatterns = [
    path('', views.TimetableView.as_view(), name='timetable'),
    path('<int:pk>/', views.SingleTimetableView.as_view(), name='single_timetable'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe')
]
