from django.shortcuts import render, redirect
from .models import Estoque, MovimentacoesEstoque
from produtos.models import Produto
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime


@login_required(login_url='logar')
def MostraEstoque(request):
    produtos_vermelho = Estoque.objects.filter(quantidade = 0)
    produtos_amarelo = Estoque.objects.filter(Q(quantidade__lt = 6) & Q(quantidade__gt = 0))
    produtos_verde = Estoque.objects.filter(quantidade__gte = 6)
    produtos = Estoque.objects.filter(nome_produto__situacao=True)
    produtos_geral = Produto.objects.all()

    context = {
        'produtos_vermelho' : produtos_vermelho,
        'produtos_amarelo' : produtos_amarelo,
        'produtos_verde' : produtos_verde,
        'produtos' : produtos,
        'produtos_geral': produtos_geral
    }

    return render(request, 'mostra_estoque.html',context)

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
    else:
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
    
def ControleEstoque(request):
    estoque_saida = MovimentacoesEstoque.objects.filter(tipo='saida')
    estoque_entrada = MovimentacoesEstoque.objects.filter(tipo='entrada')
    estoque = MovimentacoesEstoque.objects.all()
    context = {
        'estoque_saida':estoque_saida,
        'estoque_entrada':estoque_entrada,
        'estoque':estoque
    }
    return render(request, 'controle_estoque.html',context)
        
    

