from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, PessoaFisica, PessoaJuridica
from core.models import Endereco

import re


# Função utilitária para limpar números.

def limpar_numero(valor):
    """Remove tudo que não for número."""
    return re.sub(r'\D', '', valor)


# Form de cadastro de usuário.

class UserForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "email@exemplo.com"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# Form para escolher o tipo de pessoa.

class TipoPessoaForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=[("pf", "Pessoa Física"), ("pj", "Pessoa Jurídica")],
        widget=forms.RadioSelect
    )


# Forms para Pessoa Física e Pessoa Jurídica.

class PessoaFisicaForm(forms.ModelForm):

    cpf = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "000.000.000-00",
            "class": "mask-cpf",
        })
    )

    telefone_principal = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "(00) 00000-0000",
            "class": "mask-telefone",
        })
    )

    telefone_secundario = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "(00) 00000-0000",
            "class": "mask-telefone",
        })
    )

    nome_completo = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Nome Completo",
        })
    )

    rg = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Somente números"})
    )

    class Meta:
        model = PessoaFisica
        exclude = ["usuario"]

    # Limpeza e formatação.

    def clean_cpf(self):
        cpf = limpar_numero(self.cleaned_data["cpf"])
        return cpf

    def clean_rg(self):
        return limpar_numero(self.cleaned_data["rg"])

    def clean_nome_completo(self):
        nome = self.cleaned_data["nome_completo"]
        return " ".join([p.capitalize() for p in nome.split()])

    def clean_telefone_principal(self):
        return limpar_numero(self.cleaned_data["telefone_principal"])

    def clean_telefone_secundario(self):
        tel = self.cleaned_data.get("telefone_secundario")
        if not tel:
            return None
        return limpar_numero(tel)

class PessoaJuridicaForm(forms.ModelForm):

    cnpj = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "00.000.000/0000-00",
            "class": "mask-cnpj",
        })
    )

    telefone_principal = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "(00) 00000-0000",
            "class": "mask-telefone",
        })
    )

    telefone_secundario = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "(00) 00000-0000",
            "class": "mask-telefone",
        })
    )

    razao_social = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Razão Social",
        })
    )

    nome_fantasia = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Nome Fantasia",
        })
    )

    class Meta:
        model = PessoaJuridica
        exclude = ["usuario"]

    # Limpeza e formatação.

    def clean_cnpj(self):
        cnpj = limpar_numero(self.cleaned_data["cnpj"])
        return cnpj

    def clean_razao_social(self):
        texto = self.cleaned_data["razao_social"]
        return " ".join([p.capitalize() for p in texto.split()])

    def clean_nome_fantasia(self):
        texto = self.cleaned_data["nome_fantasia"]
        return " ".join([p.capitalize() for p in texto.split()])

    def clean_telefone_principal(self):
        return limpar_numero(self.cleaned_data["telefone_principal"])

    def clean_telefone_secundario(self):
        tel = self.cleaned_data.get("telefone_secundario")
        if not tel:
            return None
        return limpar_numero(tel)


# Form de endereço.

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = "__all__"


# Form de foto de perfil.

class ProfileFotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["foto"]
