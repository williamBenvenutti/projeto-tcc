from django.urls import path
from .views import TelaCompra, FinalizaCompra, RemoverProduto, LimpaCarrinho, MostraTotalGasto

urlpatterns = [
    path('realizar_compras/', TelaCompra, name='realizar_compras'),
    path('finaliza_compra/', FinalizaCompra, name="finaliza_compra"),
    path('remover_produto/<int:index>', RemoverProduto, name="remover_produto"),
    path('limpar_carrinho/', LimpaCarrinho, name="limpar_carrinho"),
    path('mostra_gasto/', MostraTotalGasto, name="mostra_gasto"),
]