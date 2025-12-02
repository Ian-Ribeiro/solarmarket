from django.urls import path
from accounts.views import CadastroWizard, FORMS, minha_conta, editar_foto
from django.contrib.auth import views as auth_views
from .views import logout_view


urlpatterns = [
    path("cadastrar/", CadastroWizard.as_view(FORMS), name="cadastrar"),
    path("minha-conta/", minha_conta, name="minha_conta"),
    path("editar-foto/", editar_foto, name="editar_foto"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/alterar_senha.html',
        success_url='/accounts/minha-conta/'
    ), name='password_change'),
]