from django.urls import path

from . import views

app_name = "utilities"

urlpatterns = [
    path('md_preview/', views.MarkdownPreview.as_view(), name='preview')
]
