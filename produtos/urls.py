from django.urls import path
from .views import MostraProdutos, CadastraProduto, EditarProduto

urlpatterns = [
    path('mostra_produtos/', MostraProdutos, name='mostra_produtos'),
    path('cadastro_produtos/', CadastraProduto, name='cadastro_produtos'),
    path('editar_produto/<int:produto_id>', EditarProduto, name='editar_produto'),
]