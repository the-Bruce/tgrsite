from django import forms
from django.contrib.auth.models import User

from .models import Rpg

BOOSTRAP_FORM_WIDGET_attrs = {
	'class': 'form-control'
}

class RpgForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(RpgForm, self).__init__(*args, **kwargs)
		for f in self.fields:
			if f != 'am_i_gm':
				self.fields[f].widget.attrs['class'] = 'form-control'
	am_i_gm = forms.BooleanField(required=False)
	am_i_gm.label = 'Add self to GMs?'
	class Meta:
		model = Rpg
		fields = ['title', 'system', 'description', 'players_wanted', 'timeslot',]
		

'''
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

class MemberForm(ModelForm):
	class Meta:
		model = Member
		fields = ['bio', 'signature']

		# neater than explicitly specifying each key as the same value
		widgets = {
			i: Textarea(attrs=BOOSTRAP_FORM_WIDGET_attrs) for i in fields
		}'''