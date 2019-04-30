from django.forms import ModelForm
from django.forms.widgets import Select, HiddenInput

from .models import NotificationSubscriptions

BOOTSTRAP_FORM_WIDGET_attrs = {
    'class': 'form-control'
}


class SubscriptionForm(ModelForm):
    class Meta:
        model = NotificationSubscriptions

        fields = ['member', 'newsletter', 'message', 'rpg_join', 'rpg_leave', 'rpg_kick', 'rpg_add', 'forum_reply',
                  'other']

        widgets = {
            'member': HiddenInput(),
            'newsletter': Select(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'message': Select(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'rpg_join': Select(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'rpg_leave': Select(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'rpg_kick': Select(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'rpg_add': Select(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'forum_reply': Select(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'other': Select(attrs=BOOTSTRAP_FORM_WIDGET_attrs)
        }
