"""
Forms that will be used for various user actions, such as language selection on
the main page, user registration or authentification.
"""
from django import forms
from django.contrib.auth.models import User
from .models import Language


class SelectLangForm(forms.Form):
    natlang = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        label="Natural Language:",
        to_field_name="code")
    conlang = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        label="Constructed Language:",
        to_field_name="code")


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
