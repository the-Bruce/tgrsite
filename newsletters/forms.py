from django.forms import ModelForm, TextInput, Textarea

from .models import Newsletter

BOOTSTRAP_FORM_WIDGET_attrs = {
	'class': 'form-control'
}

class NewsletterForm(ModelForm):
	class Meta:
		model = Newsletter
		fields = ['title', 'body', 'desc']
		widgets = {
				'title': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
				'body': Textarea(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
				'desc': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs)
				}
