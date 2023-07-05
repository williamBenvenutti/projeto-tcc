from django.shortcuts import render
from colaboradores.models import Colaborador
from produtos.models import Produto
from compras.models import RegistroCompra, ItemCompra
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime

def GerarRelatorios(request):

    produtos = Produto.objects.all()
    colabs = Colaborador.objects.all()

    context = {
        'colabs' : colabs,
        'produtos' : produtos
    }
    return render(request, "gerar_relatorios.html", context)
    
def RelatorioColab(request):
    if request.method == 'POST':
        colab_id = request.POST.get('colaborador')
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')
        
        funcionario = Colaborador.objects.get(id=colab_id)
        compras = RegistroCompra.objects.filter(colab_id=funcionario)

        if data_inicial and data_final:
            data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
            data_final = datetime.strptime(data_final, '%Y-%m-%d')
            
            compras = compras.filter(data_compra__range=(data_inicial, data_final))

        itens = ItemCompra.objects.filter(compra__in=compras)
        
        context = {
            'funcionario': funcionario,
            'compras': compras,
            'itens': itens
        }

        template = get_template('template_relatorio.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="relatorio.pdf"'

        pisa.CreatePDF(html, dest=response)

        return response
    

def RelatorioProduto(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')

        produto = Produto.objects.get(id=produto_id)
        compras = RegistroCompra.objects.filter(produtos__id=produto_id)

        if data_inicial and data_final:
            data_inicial = datetime.strptime(data_inicial, '%y-%m-%d')
            data_final = datetime.strptime(data_final, '%y-%m-%d')

            compras = compras.filter(data_compra__range=(data_inicial, data_final))

        itens_compra = ItemCompra.objects.filter(produto__id=produto_id)

        venda_total = 0
        quantidade_vendida = 0
        for item in itens_compra:
            venda_total += item.quantidade * item.preco_individual
            quantidade_vendida += item.quantidade


        context = {
            'produto': produto,
            'compras': compras,
            'itens_compra': itens_compra,
            'venda_total': venda_total,
            'quantidade_vendida' : quantidade_vendida
        }

        template = get_template('template_relatorio_produto.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename=relatorio_produto.pdf'

        pisa.CreatePDF(html, dest=response)

        return response


