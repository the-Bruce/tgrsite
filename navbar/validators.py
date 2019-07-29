from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import deconstruct
from django.utils.translation import gettext as _
import re

regex_format = r"^\/(([a-z0-9_\-])+\/)*(([a-z0-9_\-\.])+\.[a-z0-9]{2,4})?$"


@deconstruct.deconstructible
class LocalableURLValidator(validators.URLValidator):
    relative_re = re.compile(regex_format, re.IGNORECASE)
    message = _('Enter a valid absolute or relative URL.')
    description = _("URL that can be absolute or relative")

    def __call__(self, value):
        print("validate")
        try:
            super().__call__(value)
        except ValidationError:
            print("relative")
            print(value)
            a = self.relative_re.match(value)
            print(a)
            if not a:
                raise ValidationError("Invalid URL")


class LocalableURLFormField(forms.URLField):
    default_validators = [LocalableURLValidator()]

    relative_re = re.compile(regex_format, re.IGNORECASE)

    def to_python(self, value):
        if self.relative_re.match(value):
            return value
        else:
            return super().to_python(value)


class LocalableURLField(models.URLField):
    default_validators = [LocalableURLValidator()]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed
        # twice.
        return super().formfield(**{
            'form_class': LocalableURLFormField,
            **kwargs,
        })
