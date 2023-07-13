from django.urls import path
from .views import MostraEstoque, AdicionaEstoque, RemoverEstoque, ControleEstoque


urlpatterns = [
    path('mostra_estoque/', MostraEstoque, name='mostra_estoque'),
    path('mostra_estoque/adiciona_estoque/<int:produto_id>/', AdicionaEstoque, name='adiciona_estoque'),
    path('mostra_estoque/remove_estoque/<int:produto_id>/', RemoverEstoque, name='remove_estoque'),
    path('controle_estoque/', ControleEstoque, name='controle_estoque')
]