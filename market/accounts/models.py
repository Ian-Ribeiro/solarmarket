from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        default='profiles/default.png'
    )

    def __str__(self):
        return self.user.username


class Pessoa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    telefone_principal = models.CharField(max_length=20)
    telefone_secundario = models.CharField(max_length=20, blank=True, null=True)
    site = models.URLField(blank=True, null=True)

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

    def __str__(self):
        return self.nome_fantasia