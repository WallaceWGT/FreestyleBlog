"--wallace--"

from django.forms import forms
from django.forms import fields
from django.forms import widgets
from repository.models import *

class TroubleForm(forms.Form):
    title = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control','name':'title'}))

    detail = fields.CharField(
        widget=widgets.TextInput(attrs={'id':'trouble','name':'trouble'}),required=False
    )
    image = fields.ImageField(
        widget=widgets.FileInput(attrs={'name':'troubleImage'}),required=False
    )


class DearTroubleForm(forms.Form):
    dear_detail = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'dear-trouble','name':'dear_detail'}),required=False
    )

