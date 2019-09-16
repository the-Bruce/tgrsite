from django.views.generic import ListView
from .models import GalleryImage


class Index(ListView):
    model = GalleryImage
    template_name = 'gallery/index.html'
    context_object_name = "images"
