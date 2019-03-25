from django.forms import ModelForm, Textarea, TextInput

from .models import Thread, Response

# CSS class to add to every form widget to make bootstrap nice
BOOTSTRAP_FORM_WIDGET_attrs = {
    'class': 'form-control'
}

MD_INPUT = {
    'class': 'markdown-input'
}


class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'body']
        widgets = {
            'title': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'body': Textarea(attrs=MD_INPUT),
        }


# Like the thread edit form but also has a field for location
# to allow users to move their threads
class ThreadEditForm(ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'body', 'forum']
        widgets = {
            'title': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
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
