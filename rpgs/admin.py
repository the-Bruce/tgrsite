from django.contrib import admin

from .models import Rpg, Tag, TabletopCoinRequirement


class RpgAdmin(admin.ModelAdmin):
    autocomplete_fields = ('game_masters','members', 'tags')

class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Rpg, RpgAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TabletopCoinRequirement)
