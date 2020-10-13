import datetime

from django.forms import ModelForm, SelectDateWidget, NumberInput, ModelMultipleChoiceField

from .models import Suggestion, Record, Loan


class SelectDate(SelectDateWidget):
    template_name = "inventory/widget/date.html"


class NamedModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


BOOTSTRAP_FORM_WIDGET_attrs = {
}
QUANTITY_attrs = {
    'min': 1
}


class RecordForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['acquired'].initial = datetime.date.today()

    class Meta:
        model = Record
        fields = ['name', 'description', 'quantity', 'image', 'acquired', 'owner']
        widgets = {
            'quantity': NumberInput(attrs=QUANTITY_attrs),
            'acquired': SelectDate(years=range(datetime.date.today().year - 9, datetime.date.today().year + 1)),
        }


class SuggestionForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ['name', 'justification', 'context', 'link']


class LoanRequestForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if 'inv_' in kwargs:
            inv = kwargs['inv_']
            del kwargs['inv_']
        else:
            raise NotImplementedError("Must define inv_ or incorrect results can be returned")

        super().__init__(*args, **kwargs)
        self.fields['items'].queryset = Record.objects.filter(inventory=inv, owner__isnull=True)
        self.fields['start_date'].initial = datetime.date.today()
        self.fields['end_date'].initial = datetime.date.today() + datetime.timedelta(days=7)

    class Meta:
        model = Loan
        fields = ['items', 'start_date', 'end_date']
        field_classes = {
            'items': NamedModelMultipleChoiceField,
        }
        widgets = {
            'start_date': SelectDate(years=range(datetime.date.today().year, datetime.date.today().year + 10)),
            'end_date': SelectDate(years=range(datetime.date.today().year, datetime.date.today().year + 10)),
        }
        help_texts = {
            'items': 'Use Ctrl to select multiple items'
        }

    def clean(self):
        cleaned_data = super().clean()
        # print(cleaned_data)
        if not self.is_bound:  # Stop further processing.
            return

        exclude = []
        if self.instance:
            exclude.append(self.instance.id)

        unavailable = []
        for item in cleaned_data['items']:
            assert isinstance(item, Record)
            if not item.can_be_borrowed(cleaned_data['start_date'], cleaned_data['end_date'], exclude):
                unavailable.append(item.name)
        if len(unavailable) > 0:
            error = (", ".join(unavailable)) + " not available for loan between those dates"
            self.add_error('items', error)

        if cleaned_data['end_date'] < cleaned_data['start_date']:
            self.add_error('end_date', "End date must be after start date")

        if cleaned_data['start_date'] < datetime.date.today():
            self.add_error('start_date', "Start date must be in the future")

        return cleaned_data


class LoanNotesForm(ModelForm):
    class Meta:
        model = Loan
        fields = ['notes']
