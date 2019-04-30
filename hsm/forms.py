from django import forms
from django.contrib.auth.models import User

from hsm.models import Guest, Booking, Organization


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        exclude = ['visa']


class EditBookingForm(forms.ModelForm):
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


class StatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user', 'paid', 'left_to_pay']


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name']