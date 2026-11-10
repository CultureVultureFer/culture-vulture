from django import forms

from .models import username_validator


class OrganizationRegisterForm(forms.Form):
    # Ista pravila kao Organization.name. Postojeći naziv je u redu: organizator se tada pridruži toj organizaciji.
    name = forms.CharField(max_length=150, validators=[username_validator])
