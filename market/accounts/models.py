from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from validate_docbr import CPF, CNPJ


# ---------------------------------------------------------
# VALIDADORES
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# FUNÇÕES UTILITÁRIAS
# ---------------------------------------------------------

def formatar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"


def formatar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"


def formatar_telefone(telefone):
    nums = re.sub(r'\D', '', telefone)
    if len(nums) == 10:
        return f"({nums[:2]}) {nums[2:6]}-{nums[6:]}"
    elif len(nums) == 11:
        return f"({nums[:2]}) {nums[2:7]}-{nums[7:]}"
    return telefone


def capitalizar(texto):
    return " ".join([palavra.capitalize() for palavra in texto.split()])


# ---------------------------------------------------------
# MODELO DE PERFIL
# ---------------------------------------------------------

class Profile(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
        ('AD', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    foto = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    tipo_usuario = models.CharField(
        max_length=2,
        choices=TIPO_USUARIO_CHOICES,
        default='PF'
    )

    def foto_url(self):
        if self.foto:
            return self.foto.url
        return '/static/img/default.png'

    def __str__(self):
        return self.user.username


# ---------------------------------------------------------
# MODELO BASE PARA PESSOAS
# ---------------------------------------------------------

class Pessoa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    telefone_principal = models.CharField(max_length=20)
    telefone_secundario = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.telefone_principal = formatar_telefone(self.telefone_principal)

        if self.telefone_secundario:
            self.telefone_secundario = formatar_telefone(self.telefone_secundario)

        super().save(*args, **kwargs)

    @property
    def email_usuario(self):
        return self.usuario.email


# ---------------------------------------------------------
# MODELO PARA PESSOA FÍSICA
# ---------------------------------------------------------

class PessoaFisica(Pessoa):
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[validar_cpf]
    )

    nome_completo = models.CharField(max_length=150)
    data_nascimento = models.DateField()

    rg = models.CharField(
        max_length=20,
        validators=[validar_rg]
    )

    def save(self, *args, **kwargs):
        self.cpf = formatar_cpf(self.cpf)
        self.rg = re.sub(r'\D', '', self.rg)
        self.nome_completo = capitalizar(self.nome_completo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_completo


# ---------------------------------------------------------
# MODELO PARA PESSOA JURÍDICA
# ---------------------------------------------------------

class PessoaJuridica(Pessoa):
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        validators=[validar_cnpj]
    )

    razao_social = models.CharField(max_length=150)
    nome_fantasia = models.CharField(max_length=150)
    site = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.cnpj = formatar_cnpj(self.cnpj)
        self.razao_social = capitalizar(self.razao_social)
        self.nome_fantasia = capitalizar(self.nome_fantasia)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_fantasia