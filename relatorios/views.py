from django.shortcuts import render, redirect
from colaboradores.models import Colaborador
from produtos.models import Produto
from compras.models import RegistroCompra, ItemCompra
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime, date, timedelta
from django.contrib import messages

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
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    if request.method == 'POST':
        colab_id = request.POST.get('colaborador')
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')
        
        funcionario = Colaborador.objects.get(id=colab_id)
        compras = RegistroCompra.objects.filter(colab_id=funcionario)

        add_dia = timedelta(days=1)

        if data_inicial and data_final:
            data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
            data_final = datetime.strptime(data_final, '%Y-%m-%d')

            if(data_inicial > data_final):
                messages.error(request, 'Data inválida')
                return redirect('gerar_relatorios')

            compras = compras.filter(data_compra__range=(data_inicial, data_final+add_dia))

        itens = ItemCompra.objects.filter(compra__in=compras)
        venda_total = 0
        for item in itens:
            venda_total += item.quantidade * item.preco_individual

             
        venda_total_formatada = locale.currency(venda_total, grouping=True)

        for produto in itens:
            produto.preco_individual_formatado = locale.currency(produto.preco_individual, grouping=True, symbol=True)


        context = {
            'funcionario': funcionario,
            'compras': compras,
            'itens': itens,
            'venda_total' : venda_total,
            'venda_total_formatada' : venda_total_formatada,
            'data_inicial': data_inicial, 
            'data_final': data_final, 
        }

        template = get_template('template_relatorio.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

        pisa.CreatePDF(html, dest=response)

        return response
    
def RelatorioProduto(request):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')
        print(produto_id)
        produto = Produto.objects.get(id=produto_id)
        compras = RegistroCompra.objects.filter(produtos__id=produto_id)

        add_dia = timedelta(days=1)

        if data_inicial and data_final:
            data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
            data_final = datetime.strptime(data_final, '%Y-%m-%d')

            if(data_inicial > data_final):
                messages.error(request, 'Data inválida')
                return redirect('gerar_relatorios')

            compras = compras.filter(data_compra__range=(data_inicial, data_final+add_dia))

        itens_compra = ItemCompra.objects.filter(produto__id=produto_id)

        venda_total = 0
        quantidade_vendida = 0
        for item in itens_compra:
            venda_total += item.quantidade * item.preco_individual
            quantidade_vendida += item.quantidade

        venda_total_formatada = locale.currency(venda_total, grouping=True)


        context = {
            'produto': produto,
            'compras': compras,
            'itens_compra': itens_compra,
            'venda_total_formatada': venda_total_formatada,
            'quantidade_vendida' : quantidade_vendida,
            'data_inicial': data_inicial, 
            'data_final': data_final, 
        }

        template = get_template('template_relatorio_produto.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=relatorio_produto.pdf'

        pisa.CreatePDF(html, dest=response)

        return response
    

def GerarRelatorioCompras(request):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if request.method == 'POST':
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')
        
        try:
            data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
            data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
            add_dia = timedelta(days=1)
        except:
            return redirect('gerar_relatorios')
        
        if(data_inicial > data_final):
                messages.error(request, 'Data inválida')
                return redirect('gerar_relatorios')
        
        compras = RegistroCompra.objects.filter(data_compra__range=(data_inicial, data_final+add_dia))
        itens = ItemCompra.objects.filter(compra__in=compras)

        venda_total = 0

        for item in itens:
            venda_total += item.quantidade * item.preco_individual

        venda_total_formatada = locale.currency(venda_total, grouping=True, symbol=True)
        

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        for produto in itens:
            produto.preco_individual_formatado = locale.currency(produto.preco_individual, grouping=True, symbol=True)

        context = {
            'compras': compras,
            'itens': itens,
            'data_inicial': data_inicial, 
            'data_final': data_final, 
            'venda_total_formatada' : venda_total_formatada
        }

        data_inicial_str = data_inicial.strftime('%Y-%m-%d')
        data_final_str = data_final.strftime('%Y-%m-%d')

        template = get_template('template_relatorio_compras.html')
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="relatorio_compras_{data_inicial_str}_{data_final_str}.pdf"'

        pisa.CreatePDF(html, dest=response)

        return response