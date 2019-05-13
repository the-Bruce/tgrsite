from django.urls import path

from . import views

app_name = "minutes"
urlpatterns = [
    path("<path:folder>/<str:name>/",views.MeetingDetail.as_view(), name="meeting_detail"),

    path("<int:pk>/", views.meetingBounce), # Shortcut as pk is technically sufficient

]