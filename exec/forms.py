from django.forms import ModelForm, Textarea

from .models import ExecRole

MD_INPUT = {
    'class': 'markdown-input'
}


class ExecBioForm(ModelForm):
    class Meta:
        model = ExecRole
        fields = ['bio']
