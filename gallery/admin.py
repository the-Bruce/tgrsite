from django.contrib import admin

from .models import GalleryImage

class GalleryImageAdmin(admin.ModelAdmin):

	list_display = ('caption', 'filename')

	model = GalleryImage
	fields = ('filename', 'caption', 'as_img')
	readonly_fields = ('as_img',)

admin.site.register(GalleryImage, GalleryImageAdmin)
