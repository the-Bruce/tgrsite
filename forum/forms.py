from django.forms import ModelForm, Textarea, TextInput

from .models import Thread, Response

BOOSTRAP_FORM_WIDGET_attrs = {
	'class': 'form-control'
}

class ThreadForm(ModelForm):
	class Meta:
		model = Thread
		fields = ['title', 'body']
		widgets = {
			'title': TextInput(attrs=BOOSTRAP_FORM_WIDGET_attrs),
			'body': Textarea(attrs=BOOSTRAP_FORM_WIDGET_attrs),
		}

class ResponseForm(ModelForm):
	class Meta:
		model = Response
		fields = ['body']
		widgets = {
			'body': Textarea(attrs=BOOSTRAP_FORM_WIDGET_attrs),
		}

		# no labels :0
		labels = {
			'body': ''
		}
