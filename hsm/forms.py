from django import forms

from hsm.models import Guest


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        exclude = ['visa']