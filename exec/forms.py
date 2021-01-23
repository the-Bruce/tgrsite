from django.forms import ModelForm, Textarea
from django.urls import reverse_lazy

from .models import ExecRole

MD_INPUT = {
    'class': 'markdown-input',
    'data-endpoint': reverse_lazy('utilities:preview_text'),
}


class ExecBioForm(ModelForm):
    class Meta:
        model = ExecRole
        fields = ['bio', 'responsibilities']
        widgets = {
            'bio': Textarea(attrs=MD_INPUT),
            'responsibilities': Textarea(attrs=MD_INPUT),
        }
