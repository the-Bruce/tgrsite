from django.contrib import admin

from .models import NotificationSubscriptions


# Register your models here.

class SubscriptionsAdmin(admin.ModelAdmin):
    readonly_fields = ('member',)
    search_fields = ('member__equiv_user__username',)


admin.site.register(NotificationSubscriptions, SubscriptionsAdmin)
