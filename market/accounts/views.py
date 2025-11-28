from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import (
    UserForm,
    TipoPessoaForm,
    PessoaFisicaForm,
    PessoaJuridicaForm,
    EnderecoForm,
    ProfileFotoForm,
)

from .models import PessoaFisica, PessoaJuridica, Profile


FORMS = [
    ("usuario", UserForm),
    ("tipo", TipoPessoaForm),
    ("pf", PessoaFisicaForm),
    ("pj", PessoaJuridicaForm),
    ("endereco", EnderecoForm),
]

TEMPLATES = {
    "usuario": "accounts/step_usuario.html",
    "tipo": "accounts/step_tipo_pessoa.html",
    "pf": "accounts/step_pessoa_fisica.html",
    "pj": "accounts/step_pessoa_juridica.html",
    "endereco": "accounts/step_endereco.html",
}


class CadastroWizard(SessionWizardView):

    def get_form_list(self):
        """Lista dinâmica corrigida sem loops e sem erros."""

        base_forms = {
            "usuario": UserForm,
            "tipo": TipoPessoaForm,
            "pf": PessoaFisicaForm,
            "pj": PessoaJuridicaForm,
            "endereco": EnderecoForm,
        }

        # Detecta escolha do tipo
        tipo = None
        try:
            tipo_data = self.storage.get_step_data("tipo")
            if tipo_data:
                tipo = tipo_data.get("tipo-tipo")
        except Exception:
            pass

        # Remove o passo oposto
        if tipo == "pf":
            base_forms.pop("pj", None)
        elif tipo == "pj":
            base_forms.pop("pf", None)

        return base_forms

    def get_template_names(self):
        step = self.steps.current

        # Fallback caso o Wizard avance para um step removido
        if step not in TEMPLATES:
            return ["accounts/cadastro_usuario.html"]

        return [TEMPLATES[step]]

    def done(self, form_list, **kwargs):
        user_form = self.get_form(step="usuario",
            data=self.storage.get_step_data("usuario"),
            files=self.storage.get_step_files("usuario"))
        user = user_form.save()

        if not hasattr(user, "profile"):
            Profile.objects.create(user=user)

        tipo_data = self.get_cleaned_data_for_step("tipo")
        tipo = tipo_data.get("tipo")

        if tipo == "pf":
            pf_data = self.get_cleaned_data_for_step("pf")
            PessoaFisica.objects.create(
                usuario=user,
                nome=pf_data.get("nome"),
                cpf=pf_data.get("cpf"),
                data_nascimento=pf_data.get("data_nascimento"),
                rg=pf_data.get("rg"),
                email=user.email,
                telefone_principal=pf_data.get("telefone_principal"),
                telefone_secundario=pf_data.get("telefone_secundario"),
                site=pf_data.get("site"),
            )
        elif tipo == "pj":
            pj_data = self.get_cleaned_data_for_step("pj")
            PessoaJuridica.objects.create(
                usuario=user,
                cnpj=pj_data.get("cnpj"),
                razao_social=pj_data.get("razao_social"),
                nome_fantasia=pj_data.get("nome_fantasia"),
                email=user.email,
                telefone_principal=pj_data.get("telefone_principal"),
                telefone_secundario=pj_data.get("telefone_secundario"),
                site=pj_data.get("site"),
            )

        endereco_data = self.get_cleaned_data_for_step("endereco")

        return render(self.request, "accounts/cadastro_concluido.html", {"user": user})



@login_required
def minha_conta(request):
    profile = request.user.profile  # acessa o perfil vinculado ao usuário
    return render(request, "accounts/minha_conta.html", {"profile": profile})


@login_required
def editar_foto(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileFotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("minha_conta")
    else:
        form = ProfileFotoForm(instance=profile)

    return render(request, "accounts/editar_foto.html", {"form": form})
