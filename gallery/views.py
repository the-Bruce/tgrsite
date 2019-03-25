from django.shortcuts import render

from .models import GalleryImage


def index(request):
    images = GalleryImage.objects.all()
    return render(request, 'gallery/index.html', {'images': images})
