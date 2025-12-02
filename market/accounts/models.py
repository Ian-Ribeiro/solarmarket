from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from validate_docbr import CPF, CNPJ



def validar_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError('CPF inválido.')

def validar_rg(value):
    rg = re.sub(r'[^0-9]', '', value)
    if len(rg) < 5 or len(rg) > 12:
        raise ValidationError('RG inválido.')

def validar_cnpj(value):
    cnpj = CNPJ()
    if not cnpj.validate(value):
        raise ValidationError('CNPJ inválido.')




class Profile(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
        ('AD', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Foto padrão agora vem do STATIC
    foto = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    # Campo para identificar o tipo de usuário
    tipo_usuario = models.CharField(
        max_length=2,
        choices=TIPO_USUARIO_CHOICES,
        default='PF'
    )

    def foto_url(self):
        """Retorna a foto do usuário OU a imagem padrão no static."""
        if self.foto:
            return self.foto.url
        return '/static/img/default.png'

    def __str__(self):
        return self.user.username


class Pessoa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    telefone_principal = models.CharField(max_length=20)
    telefone_secundario = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        abstract = True


class PessoaFisica(Pessoa):
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=150)
    data_nascimento = models.DateField()
    rg = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class PessoaJuridica(Pessoa):
    cnpj = models.CharField(max_length=14, unique=True)
    razao_social = models.CharField(max_length=150)
    nome_fantasia = models.CharField(max_length=150)
    site = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome_fantasia