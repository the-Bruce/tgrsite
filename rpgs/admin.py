from django.contrib import admin

from .models import Rpg, Session

class SessionsInline(admin.StackedInline):
	model = Session
	extra = 0

class RpgAdmin(admin.ModelAdmin):
	inlines = [SessionsInline]
	list_display=('title', 'creator', 'tags_list')

admin.site.register(Rpg, RpgAdmin)
admin.site.register(Session)
