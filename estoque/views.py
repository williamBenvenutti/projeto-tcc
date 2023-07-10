from django.shortcuts import render, redirect, get_object_or_404
from .models import Estoque
from produtos.models import Produto
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages

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

def AdicionaEstoque(request, produto_id):
    if request.method == 'POST':
        quantidade = request.POST.get('quantidade')

        if not quantidade:
            messages.error(request, 'Digite um valor válido!')
            return redirect('mostra_estoque')

        try:
            produto = get_object_or_404(Estoque, id=produto_id)
            produto.quantidade += int(quantidade)
            produto.save()
        except (ValueError, Estoque.DoesNotExist):
            messages.error(request, 'Produto não encontrado!')
            return redirect('mostra_estoque')


        return redirect('mostra_estoque')
    else:
        return redirect('mostra_estoque')
    

