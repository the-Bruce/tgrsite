from django import forms
from django.contrib.auth.models import User

from .models import Rpg

class RpgForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(RpgForm, self).__init__(*args, **kwargs)
		for f in self.fields:
			if f != 'am_i_gm' and f != 'is_in_the_past':
				self.fields[f].widget.attrs['class'] = 'form-control'
			if f == 'is_in_the_past':
				self.fields[f].label = 'Has this finished?'
	am_i_gm = forms.BooleanField(required=False)
	am_i_gm.label = 'Are you running this?'
	class Meta:
		model = Rpg
		fields = ['title', 'system', 'description', 'players_wanted', 'timeslot', 'is_in_the_past',]
	tags = forms.CharField(required=False)

# Unused so far
class RpgManageForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(RpgManageForm, self).__init__(*args, **kwargs)
		for f in self.fields:
			self.fields[f].widget.attrs['class'] = 'form-control'
	class Meta:
		model = Rpg
		fields = ['members']
