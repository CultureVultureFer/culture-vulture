from django import forms

from .models import username_validator


class OrganizationRegisterForm(forms.Form):
    # Same rules as Organization.name. An existing name is fine: the organizer then joins that organization.
    name = forms.CharField(max_length=150, validators=[username_validator])
