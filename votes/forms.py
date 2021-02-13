from django.forms import ModelForm, Textarea
from django.urls import reverse_lazy

from .models import Election, Candidate

MD_INPUT_SAFE = {
    'class': 'markdown-input',
    'data-endpoint': reverse_lazy('utilities:preview_safe'),
}

MD_INPUT_TEXT = {
    'class': 'markdown-input',
    'data-endpoint': reverse_lazy('utilities:preview_text'),
}

class ElectionForm(ModelForm):
    class Meta:
        model = Election
        fields = ['name', 'description', 'vote_type', 'max_votes', 'seats', 'open']
        widgets = {'description': Textarea(attrs=MD_INPUT_SAFE)}


class CandidateForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'description', 'state']
        widgets = {'description': Textarea(attrs=MD_INPUT_TEXT)}
