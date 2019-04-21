from django import forms
from django.contrib.auth.models import User

from hsm.models import Guest, Booking


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        exclude = ['visa']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class GuestsForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['full_name', 'passport']