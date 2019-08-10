from django.contrib import admin

from .models import GalleryImage


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image')

    model = GalleryImage
    fields = ('image', 'caption', 'as_img')
    readonly_fields = ('as_img',)


admin.site.register(GalleryImage, GalleryImageAdmin)
