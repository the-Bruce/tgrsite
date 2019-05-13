from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea, TextInput, EmailInput, PasswordInput, ValidationError

from .models import Member

BOOTSTRAP_FORM_WIDGET_attrs = {
    'class': 'form-control'
}

MD_INPUT = {
    'class': 'markdown-input'
}


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'password': PasswordInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        # they all have the same format (TextInputs)
        widgets = {
            i: TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs) for i in fields
        }
        # ...except this one
        widgets['email'] = EmailInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs)

        help_texts = {
            'first_name': "Please consider adding your name to help others recognise you"
        }

    def clean(self):
        data = self.cleaned_data
        if 'username' not in data:
            raise ValidationError('')

        if len(data['username']) > 32:
            self.add_error('username', ValidationError('Username must be 32 characters or fewer.'))


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'email': EmailInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'password': PasswordInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
        }

        help_texts = {
            'username': 'Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.'
        }

    def clean(self):
        data = self.cleaned_data
        if 'username' not in data:
            raise ValidationError('')

        if len(data['username']) > 32:
            self.add_error('username', ValidationError('Username must be 32 characters or fewer.'))


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['discord', 'bio', 'signature', 'official_photo_url']

        widgets = {
            'discord': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'bio': Textarea(attrs=MD_INPUT),
            'signature': Textarea(attrs=MD_INPUT),
            'official_photo_url': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs)
        }

        help_texts = {
            'official_photo_url': 'Provide a URL for a real photo of you. This is only shown on the exec page and '
                                  'only if you are a member of exec! Gravatar is used by the rest of the site for '
                                  'profile pictures - for more information see this '
                                  '<a href="https://github.com/the-Bruce/tgrsite/wiki/Gravatar">guide</a>.',
            'discord': 'Add your discord ID to aid recognition on the society discord'
        }
