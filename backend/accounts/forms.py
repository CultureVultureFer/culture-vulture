from django import forms

from .models import User, username_validator


class OrganizerForm(forms.Form):
    name = forms.CharField(max_length=150)

    def __init__(self, data, *, user: User):
        super().__init__(data)
        self.user = user

    def clean_name(self):
        name = " ".join(self.cleaned_data["name"].split())
        username_validator(name)
        taken = User.objects.filter(username__iexact=name).exclude(pk=self.user.pk).exists()
        if taken:
            raise forms.ValidationError("An organization with this name already exists.")
        return name
