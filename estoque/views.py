from django.shortcuts import render, redirect
from .models import Estoque
from produtos.models import Produto
from django.db.models import Q

def MostraEstoque(request):
    produtos_vermelho = Estoque.objects.filter(Q(quantidade__lte = 3))
    produtos_amarelo = Estoque.objects.filter(Q(quantidade__lt = 6) & Q(quantidade__gt = 3))
    produtos_verde = Estoque.objects.filter(Q(quantidade__gte = 6))
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

        produto = Estoque.objects.get(id=produto_id)

        Estoque.objects.filter(id=produto_id).update(
            quantidade = int(produto.quantidade) + int(quantidade)
        )
        return redirect('mostra_estoque')
    else:
        return redirect('mostra_estoque')
    

