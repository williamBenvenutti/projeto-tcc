from django.urls import path
from .views import MostraEstoque, AdicionaEstoque, RemoverEstoque, ControleEstoque, MovimentaEstoque


urlpatterns = [
    path('mostra_estoque/', MostraEstoque, name='mostra_estoque'),
    path('movimenta_estoque/<int:produto_id>/', MovimentaEstoque, name='movimenta_estoque'),
    path('adiciona_estoque/<int:produto_id>/', AdicionaEstoque, name='adiciona_estoque'),
    path('remove_estoque/<int:produto_id>/', RemoverEstoque, name='remove_estoque'),
    path('controle_estoque/', ControleEstoque, name='controle_estoque')
]