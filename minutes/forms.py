from django.forms import ModelForm, Textarea, TextInput, DateInput, Select

from .models import Meeting, Folder

# CSS class to add to every form widget to make bootstrap nice
BOOTSTRAP_FORM_WIDGET_attrs = {
    'class': 'form-control'
}

MD_INPUT = {
    'class': 'markdown-input'
}


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['name', 'title', 'folder', 'body', 'date']
        widgets = {
            'name': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'title': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'folder': Select(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'body': Textarea(attrs=MD_INPUT),
            'date': DateInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs)
        }
