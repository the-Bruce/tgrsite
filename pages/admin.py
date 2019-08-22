from django.contrib import admin

from .models import Page, BreadcrumbParents


class BreadcrumbInline(admin.TabularInline):
    model = BreadcrumbParents
    extra = 0


class PageAdmin(admin.ModelAdmin):
    inlines = [BreadcrumbInline]


admin.site.register(Page, PageAdmin)
