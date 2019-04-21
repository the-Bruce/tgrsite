import datetime

from django.forms import ModelForm, TextInput, Textarea, URLInput, SelectDateWidget, SelectMultiple, NumberInput, Select

from .models import Suggestion, Record, Loan


class SelectDate(SelectDateWidget):
    template_name = "inventory/widget/date.html"


BOOTSTRAP_FORM_WIDGET_attrs = {
    'class': 'form-control'
}
QUANTITY_attrs = {
    'min': 1,
    'class': 'form-control'
}


class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['name', 'description', 'quantity', 'image', 'acquired', 'owner']
        widgets = {
            'name': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'quantity': NumberInput(attrs=QUANTITY_attrs),
            'description': Textarea(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'image': URLInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'acquired': SelectDate(years=range(datetime.date.today().year - 9, datetime.date.today().year + 1),
                                   attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'owner': Select(attrs=BOOTSTRAP_FORM_WIDGET_attrs)
        }


class SuggestionForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ['name', 'justification', 'context', 'link']
        widgets = {
            'name': TextInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'justification': Textarea(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'context': Textarea(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'link': URLInput(attrs=BOOTSTRAP_FORM_WIDGET_attrs)
        }


class LoanRequestForm(ModelForm):
    class Meta:
        model = Loan
        fields = ['items', 'start_date', 'end_date']
        widgets = {
            'items': SelectMultiple(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'start_date': SelectDate(years=range(datetime.date.today().year - 9, datetime.date.today().year + 1),
                                     attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'end_date': SelectDate(years=range(datetime.date.today().year - 9, datetime.date.today().year + 1),
                                   attrs=BOOTSTRAP_FORM_WIDGET_attrs),
        }
