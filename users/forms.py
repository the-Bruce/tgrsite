from django.forms import ModelForm, Textarea, TextInput, EmailInput, PasswordInput
from django.contrib.auth.models import User

from .models import Member

BOOSTRAP_FORM_WIDGET_attrs = {
	'class': 'form-control'
}

class LoginForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']
		widgets = {
			'username': TextInput(attrs=BOOSTRAP_FORM_WIDGET_attrs),
			'password': PasswordInput(attrs=BOOSTRAP_FORM_WIDGET_attrs),
		}

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']

		# they all have the same format (TextInputs)
		widgets = {
			i: TextInput(attrs=BOOSTRAP_FORM_WIDGET_attrs) for i in fields
		}

		# email needs to be an email field though
		widgets['email'] = EmailInput(attrs=BOOSTRAP_FORM_WIDGET_attrs)

class SignupForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']

		widgets = {
			'username': TextInput(attrs=BOOSTRAP_FORM_WIDGET_attrs),
			'email': EmailInput(attrs=BOOSTRAP_FORM_WIDGET_attrs),
			'password': PasswordInput(attrs=BOOSTRAP_FORM_WIDGET_attrs),
		}


class MemberForm(ModelForm):
	class Meta:
		model = Member
		fields = ['bio', 'signature']

		# neater than explicitly specifying each key as the same value
		widgets = {
			i: Textarea(attrs=BOOSTRAP_FORM_WIDGET_attrs) for i in fields
		}
