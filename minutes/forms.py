from django.forms import ModelForm, Textarea

from .models import Meeting
MD_INPUT = {
    'class': 'markdown-input'
}


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['name', 'folder', 'title', 'body', 'date']
        widgets = {
            'body': Textarea(attrs=MD_INPUT),
        }
