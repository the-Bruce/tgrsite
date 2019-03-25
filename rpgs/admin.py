from django.contrib import admin

from .models import Rpg, Session, Tag


class SessionsInline(admin.StackedInline):
    model = Session
    extra = 0


class RpgAdmin(admin.ModelAdmin):
    inlines = [SessionsInline]


admin.site.register(Rpg, RpgAdmin)
admin.site.register(Session)
admin.site.register(Tag)
