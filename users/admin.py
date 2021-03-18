from functools import reduce

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from rpgs.models import Rpg
from .models import Member, Membership, VerificationRequest, Achievement, AchievementAward


def field_property(field_name, **kwargs):
    def _from_property(admin, obj=None):
        if not obj:
            return None
        rv = reduce(getattr, field_name.split("."), obj)
        return rv() if callable(rv) else rv

    for key, value in kwargs.items():
        setattr(_from_property, key, value)
    return _from_property


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'member'
    readonly_fields = ('dark', 'is_soc_member')


class MembershipInline(admin.StackedInline):
    model = Membership


class RpgInline(admin.TabularInline):
    model = Rpg
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (MemberInline,)
    save_on_top = True


class MemberAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)
    search_fields = ('equiv_user__username', 'discord')
    readonly_fields = ('dark',)
    list_display = ('username', 'discord', 'firstname', 'last_name', 'pronoun')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Membership)
admin.site.register(VerificationRequest)
admin.site.register(Achievement)
admin.site.register(AchievementAward)
