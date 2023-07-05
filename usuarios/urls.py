from django.urls import path
from .views import Login, CadastroUsuario, MostraUsuario, Dashboard, Logout, EditarUsuario, ExcluiUsuario, AlteraSenha

urlpatterns = [
    path('', Login, name='logar'),
    path('cadastro_usuario/', CadastroUsuario, name='cadastro_usuario'),
    path('mostra_usuario/', MostraUsuario, name='mostra_usuario'),
    path('editar_usuario/<int:user_id>/', EditarUsuario, name='editar_usuario'),
    path('exclui_usuario/<int:user_id>/', ExcluiUsuario, name="exclui_usuario"),
    path('altera_senha/<int:user_id>/', AlteraSenha, name="altera_senha"),
    path('dashboard/', Dashboard, name='dashboard'),
    path('logout/', Logout, name='logout'),
]