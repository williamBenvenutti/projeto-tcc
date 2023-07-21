from django.shortcuts import render
from colaboradores.models import Colaborador
from produtos.models import Produto
from compras.models import RegistroCompra, ItemCompra
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime, date
import locale


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

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        for produto in itens:
            produto.preco_individual_formatado = locale.currency(produto.preco_individual, grouping=True, symbol=True)


        context = {
            'funcionario': funcionario,
            'compras': compras,
            'itens': itens
        }

        template = get_template('template_relatorio.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

        pisa.CreatePDF(html, dest=response)

        return response
    
def RelatorioProduto(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')
        print(produto_id)
        produto = Produto.objects.get(id=produto_id)
        compras = RegistroCompra.objects.filter(produtos__id=produto_id)

        if data_inicial and data_final:
            data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
            data_final = datetime.strptime(data_final, '%Y-%m-%d')

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
        response['Content-Disposition'] = 'attachment; filename=relatorio_produto.pdf'

        pisa.CreatePDF(html, dest=response)

        return response
    

def GerarRelatorioCompras(request):
    if request.method == 'POST':
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')

        # Convertendo as strings para objetos datetime.date
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

        compras = RegistroCompra.objects.filter(data_compra__range=(data_inicial, data_final))
        itens = ItemCompra.objects.filter(compra__in=compras)

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        for produto in itens:
            produto.preco_individual_formatado = locale.currency(produto.preco_individual, grouping=True, symbol=True)

        context = {
            'compras': compras,
            'itens': itens,
            'data_inicial': data_inicial,  # Apenas a data, sem a hora
            'data_final': data_final,  # Apenas a data, sem a hora
        }

        # Formatando a data para o nome do arquivo
        data_inicial_str = data_inicial.strftime('%Y-%m-%d')
        data_final_str = data_final.strftime('%Y-%m-%d')

        template = get_template('template_relatorio_compras.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="relatorio_compras_{data_inicial_str}_{data_final_str}.pdf"'

        pisa.CreatePDF(html, dest=response)

        return response