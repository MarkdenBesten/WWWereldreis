from django import forms
from django.core.exceptions import ValidationError


class AnswerForm(forms.Form):
    Joker = forms.CharField(max_length=6)
    latitude = forms.FloatField(required=False, initial=0)
    longitude = forms.FloatField(required=False, initial=0)

