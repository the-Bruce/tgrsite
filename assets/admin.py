from django.contrib import admin

from .models import Asset


class AssetAdmin(admin.ModelAdmin):
    fields = ('name', 'assetFile')


# Register your models here.
admin.site.register(Asset, AssetAdmin)
