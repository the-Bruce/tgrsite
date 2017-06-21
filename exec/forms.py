from django.forms import ModelForm
from .models import ExecRole

class ExecBioForm(ModelForm):
	class Meta:
		model = ExecRole
		fields = ['bio']
