from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, PessoaFisica, PessoaJuridica
from core.models import Endereco


class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class TipoPessoaForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=[("pf", "Pessoa Física"), ("pj", "Pessoa Jurídica")],
        widget=forms.RadioSelect
    )


class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        exclude = ["usuario"]


class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        exclude = ["usuario"]


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = "__all__"


class ProfileFotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["foto"]