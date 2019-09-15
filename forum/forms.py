from django.forms import ModelForm, Textarea, TextInput

from .models import Thread, Response

MD_INPUT = {
    'class': 'markdown-input'
}


class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'body']
        widgets = {
            'body': Textarea(attrs=MD_INPUT),
        }


# Like the thread edit form but also has a field for location
# to allow users to move their threads
class ThreadEditForm(ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'body', 'forum']
        widgets = {
            'body': Textarea(attrs=MD_INPUT),
        }


# form that goes under a post for users to reply to
# presented as a "comment" style thing
class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ['body']
        widgets = {
            'body': Textarea(attrs=MD_INPUT),
        }

        labels = {
            'body': '',
        }
