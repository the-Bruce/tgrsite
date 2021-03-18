from django.forms import ModelForm
from django.forms.widgets import Select, HiddenInput

from .models import NotificationSubscriptions


class SubscriptionForm(ModelForm):
    class Meta:
        model = NotificationSubscriptions

        fields = ['newsletter', 'message', 'loan_request', 'rpg_join', 'rpg_leave', 'rpg_kick', 'rpg_add',
                  'rpg_new', 'forum_reply', 'achievement_got', 'other']
