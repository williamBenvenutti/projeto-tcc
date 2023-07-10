from django.urls import path
from .views import MostraEstoque, AdicionaEstoque


urlpatterns = [
    path('mostra_estoque/', MostraEstoque, name='mostra_estoque'),
    path('mostra_estoque/adiciona_estoque/<int:produto_id>/', AdicionaEstoque, name='adiciona_estoque')
]