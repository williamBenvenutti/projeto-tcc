from django.shortcuts import render, redirect
from .models import Estoque, MovimentacoesEstoque
from produtos.models import Produto
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.dateparse import parse_date


@login_required(login_url='logar')
def MostraEstoque(request):
    if request.method == 'GET':
        filtro_situacao = request.GET.get('filtro_situacao')
        filtro_nome = request.GET.get('filtro_nome')
        filtro_quantidade = request.GET.get('filtro_quantidade')
        produtos_vermelho = Estoque.objects.filter(quantidade = 0, nome_produto__situacao=True)
        produtos_amarelo = Estoque.objects.filter(Q(quantidade__lt = 6) & Q(quantidade__gt = 0), nome_produto__situacao=True)
        produtos_verde = Estoque.objects.filter(quantidade__gte = 6, nome_produto__situacao=True)
        produtos_geral = Estoque.objects.all()

        if filtro_quantidade:
            produtos_geral = produtos_geral.filter(quantidade = filtro_quantidade)
        
        if filtro_nome:
            produtos_geral = produtos_geral.filter(nome_produto__nome__icontains=filtro_nome)

        if filtro_situacao:
            if filtro_situacao == 'esgotado':
                produtos_geral = Estoque.objects.filter(quantidade = 0, nome_produto__situacao=True)
            elif filtro_situacao == 'atencao':
                produtos_geral = Estoque.objects.filter(Q(quantidade__lt = 6) & Q(quantidade__gt = 0), nome_produto__situacao=True)
            elif filtro_situacao == 'normal':
                produtos_geral = Estoque.objects.filter(quantidade__gte = 6, nome_produto__situacao=True)

        produtos_geral = produtos_geral.order_by('quantidade')

        context = {
            'produtos_vermelho' : produtos_vermelho,
            'produtos_amarelo' : produtos_amarelo,
            'produtos_verde' : produtos_verde,
            'produtos_geral': produtos_geral
        }

        return render(request, 'mostra_estoque.html',context)

def MovimentaEstoque(request, produto_id):
    produto = Estoque.objects.get(id=produto_id)
    context = {
        'produto':produto
    }
    return render(request, 'movimenta_estoque.html', context)


@login_required(login_url='logar')
def AdicionaEstoque(request, produto_id):
    if request.method == 'POST':
        quantidade = request.POST.get('quantidade')

        if not quantidade:
            messages.error(request, 'Digite um valor válido!')
            return redirect('mostra_estoque')

        try:
            produto = Estoque.objects.get(id=produto_id)
            produto.quantidade += int(quantidade)
            produto.save()

            MovimentacoesEstoque.objects.create(
                usuario = request.user,
                nome_produto = Produto.objects.get(id=produto_id),
                data_hora = datetime.now(),
                quantidade = quantidade,
                tipo = 'entrada'
            )

        except (ValueError, Estoque.DoesNotExist):
            messages.error(request, 'Produto não encontrado!')
            return redirect('mostra_estoque')

        return redirect('mostra_estoque')
    
@login_required(login_url='logar')
def RemoverEstoque(request, produto_id):
    if request.method == 'POST':
        quantidade = request.POST.get('quantidade')

        if not quantidade:
            messages.error(request, 'Digite um valor válido!')
            return redirect('mostra_estoque')

        try:
            produto = Estoque.objects.get(id=produto_id)
            produto.quantidade -= int(quantidade)
            produto.save()

            MovimentacoesEstoque.objects.create(
                usuario = request.user,
                nome_produto = Produto.objects.get(id=produto_id),
                data_hora = datetime.now(),
                quantidade = quantidade,
                tipo = 'saida'
            )

        except (ValueError, Estoque.DoesNotExist):
            messages.error(request, 'Produto não encontrado!')
            return redirect('mostra_estoque')

        return redirect('mostra_estoque')
    else:
        return redirect('mostra_estoque')
    
@login_required(login_url='logar')
def ControleEstoque(request):
    if request.method == 'GET':
        filtro_nome = request.GET.get('filtro_nome', None)
        filtro_tipo = request.GET.get('filtro_tipo', None)
        filtro_quantidade = request.GET.get('filtro_quantidade', None)
        filtro_data = request.GET.get('filtro_data', None)
        filtro_usuario = request.GET.get('filtro_usuario', None)

        estoque = MovimentacoesEstoque.objects.all()
        estoque = estoque.order_by('-data_hora')

        if filtro_nome:
            estoque = estoque.filter(nome_produto__nome__icontains=filtro_nome)
            print(estoque)

        if filtro_quantidade:
            estoque = estoque.filter(quantidade=filtro_quantidade)

        context = {
            'estoque': estoque
        }

        return render(request, 'controle_estoque.html', context)
        
    

