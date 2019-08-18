from django.forms import ModelForm, Textarea, ChoiceField

from .models import Meeting, Folder

MD_INPUT = {
    'class': 'markdown-input'
}


class MeetingForm(ModelForm):
    folder = ChoiceField(choices=sorted([(x.pk, str(x)) for x in Folder.objects.all()], key=lambda x: x[1]))

    class Meta:
        model = Meeting
        fields = ['name', 'folder', 'title', 'body', 'date']
        widgets = {
            'body': Textarea(attrs=MD_INPUT),
        }

    def clean_folder(self):
        return Folder.objects.get(pk=self.cleaned_data['folder'])