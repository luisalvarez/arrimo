from django import forms
from django.core.exceptions import ValidationError


class UpperCaseField(forms.CharField):
    def clean(self, value):
        try:
            return value.upper()
        except:
            raise ValidationError