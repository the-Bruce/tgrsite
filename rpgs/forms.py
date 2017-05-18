from django import forms
from django.contrib.auth.models import User

from .models import Rpg

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
