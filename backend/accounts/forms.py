"""
Validacija ulaznih podataka.

Prijava i registracija su ISKLJUČIVO preko Googlea, pa ovdje nema forme za
email ni lozinku: email dolazi iz Googleovog id_tokena (Google ga je
potvrdio), a lozinku nemamo.

Jedina forma je za postajanje organizatorom: korisnik je već prijavljen
Googleom i upisuje samo naziv organizacije.

Zašto Django forma, a ne ručna provjera u view-u: forme daju jednak format
grešaka po polju ({"name": ["..."]}), a frontend (react-hook-form) ih može
izravno prikazati uz polje.
"""

from django import forms

from .models import User, username_validator


class OrganizerForm(forms.Form):
    """
    POST /api/auth/register/organizer/  ->  {name}

    Ime polja `name` je isto kao u Karlovom obrascu (register-front,
    OrgRegister.jsx). Ako frontend pošalje i druga polja, backend ih ignorira.
    """

    name = forms.CharField(max_length=150)

    def __init__(self, data, *, user: User):
        super().__init__(data)
        # Trenutni korisnik: njegovo vlastito ime ne smatramo "zauzetim".
        self.user = user

    def clean_name(self):
        name = " ".join(self.cleaned_data["name"].split())  # višestruki razmaci -> jedan
        username_validator(name)
        taken = User.objects.filter(username__iexact=name).exclude(pk=self.user.pk).exists()
        if taken:
            raise forms.ValidationError("An organization with this name already exists.")
        return name
