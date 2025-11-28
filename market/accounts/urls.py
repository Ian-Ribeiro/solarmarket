from django.urls import path
from accounts.views import CadastroWizard, FORMS, minha_conta, editar_foto
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("cadastrar/", CadastroWizard.as_view(FORMS), name="cadastrar"),
    path("minha-conta/", minha_conta, name="minha_conta"),
    path("editar-foto/", editar_foto, name="editar_foto"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
]