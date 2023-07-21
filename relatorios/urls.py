from django.urls import path
from .views import GerarRelatorios, RelatorioColab, RelatorioProduto, GerarRelatorioCompras

urlpatterns =[
    path('gerar_relatorios/', GerarRelatorios, name='gerar_relatorios'),
    path('relatorio_colab/', RelatorioColab, name='relatorio_colab'),
    path('relatorio_produto/', RelatorioProduto, name='relatorio_produto'),
    path('relatorio_compras/', GerarRelatorioCompras, name='relatorio_compras'),

]