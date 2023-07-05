from django.shortcuts import render, redirect
from .models import Produto
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import locale
from django.contrib import messages


@login_required(login_url='logar')
def MostraProdutos(request):
    produtos = Produto.objects.all()
    quantidade_produtos = Produto.objects.count()
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    for produto in produtos:
        produto.preco = locale.currency(produto.preco, grouping=True, symbol=None)

    return render(request, 'mostra_produtos.html', {'produtos': produtos, 'quantidade_produtos': quantidade_produtos})



@login_required(login_url='logar')
def CadastraProduto(request):
    if request.method == 'POST':
        new_nome_produto = request.POST.get('nome_produto')
        new_codigo_de_barras = request.POST.get('codigo_de_barras')
        new_preco_produto = request.POST.get('preco_produto')

        try:
            Produto.objects.create(
                nome = new_nome_produto,
                codigo_de_barras = new_codigo_de_barras,
                preco = new_preco_produto,
            )
            return redirect('mostra_produtos')
        
        except Exception as e:
            if 'UNIQUE' in str(e):
                context = {
                    'nome_produto' : new_nome_produto,
                    'codigo_de_barras' : new_codigo_de_barras,
                    'preco_produto' : new_preco_produto
                }
                messages.error(request, 'Código de barras já existe!')
                return render(request, 'cadastro_produtos.html', context)
            else:
                messages.error(request, e)
                return render(request, 'cadastro_produtos.html')
    else:
        return render(request, 'cadastro_produtos.html')

@login_required(login_url='logar')
def EditarProduto(request, produto_id):
    if request.method == 'POST':
        new_nome_produto = request.POST.get('nome_produto')
        new_codigo_de_barras = request.POST.get('codigo_de_barras')
        new_preco_produto = request.POST.get('preco_produto')

        try:
            Produto.objects.filter(id=produto_id).update(
                nome=new_nome_produto,
                codigo_de_barras=new_codigo_de_barras,
                preco=new_preco_produto
            )
            return redirect('mostra_produtos')
        
        except Exception as e:
            if 'UNIQUE' in str(e) and ('codigo_de_barras') in str(e):
                messages.error(request, 'Código de Barras já existe!')
                return redirect('editar_produto', produto_id=produto_id)
            else:
                return HttpResponse(e)
    else:
        produtos = Produto.objects.get(id=produto_id)
        return render(request, 'editar_produto.html', {'produtos': produtos})
