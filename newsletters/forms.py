from django.forms import ModelForm, TextInput, Textarea, CheckboxInput
from django.urls import reverse_lazy

from .models import Newsletter

BOOTSTRAP_FORM_WIDGET_attrs = {
    'class': 'form-control'
}

MD_INPUT = {
    'class': 'markdown-input',
    'data-endpoint': reverse_lazy('utilities:preview_safe')
}


class NewsletterForm(ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'body', 'summary', 'ispublished']
        widgets = {
            'title': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'body': Textarea(attrs=MD_INPUT),
            'summary': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'ispublished': CheckboxInput(),
        }
