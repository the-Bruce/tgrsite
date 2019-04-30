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
    def __init__(self, *args, **kwargs):
        if 'inv_' in kwargs:
            inv = kwargs['inv_']
            del kwargs['inv_']
        else:
            raise NotImplementedError("Must define inv_ or incorrect results can be returned")

        super().__init__(*args, **kwargs)
        self.fields['items'].queryset = Record.objects.filter(inventory=inv, owner__isnull=True)

    class Meta:
        model = Loan
        fields = ['items', 'start_date', 'end_date']
        widgets = {
            'items': SelectMultiple(attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'start_date': SelectDate(years=range(datetime.date.today().year, datetime.date.today().year + 10),
                                     attrs=BOOTSTRAP_FORM_WIDGET_attrs),
            'end_date': SelectDate(years=range(datetime.date.today().year, datetime.date.today().year + 10),
                                   attrs=BOOTSTRAP_FORM_WIDGET_attrs),
        }
        help_texts = {
            'items': 'Use Ctrl to select multiple items'
        }

    def clean(self):
        super().clean()
        if not self.is_bound:  # Stop further processing.
            return
        unavailable = []
        for item in self.cleaned_data['items']:
            assert isinstance(item, Record)
            if not item.can_be_borrowed(self.cleaned_data['start_date'], self.cleaned_data['end_date']):
                unavailable.append(item.name)
        if len(unavailable) > 0:
            error = (", ".join(unavailable)) + " not available for loan between those dates"
            self.add_error('items', error)

        if self.cleaned_data['start_date'] < datetime.date.today():
            self.add_error('start_date', "Start date must be in the future")
        if self.cleaned_data['end_date'] < self.cleaned_data['start_date']:
            self.add_error('end_date', "End date must be after start date")
