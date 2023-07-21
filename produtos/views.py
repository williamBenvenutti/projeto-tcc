from django.shortcuts import render, redirect
from .models import Produto
from estoque.models import Estoque
from django.contrib.auth.decorators import login_required
import locale
from django.contrib import messages
from django.db.models import F


@login_required(login_url='logar')
def MostraProdutos(request):
    if request.method == 'GET':
        filtro_nome = request.GET.get('filtro_nome', None)
        filtro_codigo_barras = request.GET.get('filtro_codigo_barras', None)
        filtro_preco = request.GET.get('filtro_preco', None)
        filtro_situacao = request.GET.get('filtro_situacao', None)

        print(filtro_situacao)

        produtos = Produto.objects.all()

        if filtro_nome:
            produtos = produtos.filter(nome__icontains=filtro_nome)

        if filtro_codigo_barras:
            produtos = produtos.filter(codigo_de_barras__icontains=filtro_codigo_barras)

        if filtro_preco:
            produtos = produtos.filter(preco=ConverteValorCifrao(filtro_preco))

        if filtro_situacao:
            if filtro_situacao == 'ativo':
                produtos = produtos.filter(situacao=True)
            elif filtro_situacao == 'inativo':
                produtos = produtos.filter(situacao=False)


        produtos = produtos.order_by('-situacao', 'nome')

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        for produto in produtos:
            produto.preco = locale.currency(produto.preco, grouping=True, symbol=True)

        return render(request, 'mostra_produtos.html', {'produtos': produtos})
        


@login_required(login_url='logar')
def CadastraProduto(request):
    if request.method == 'POST':
        new_nome_produto = request.POST.get('nome_produto')
        new_codigo_de_barras = request.POST.get('codigo_de_barras')
        new_preco_produto = request.POST.get('preco_produto')
        new_situacao = True if request.POST.get('situacao') else False
        new_categoria = request.POST.get('categoria')

        try:
            novo_produto = Produto(
                nome = new_nome_produto,
                codigo_de_barras = new_codigo_de_barras,
                preco = ConverteValorCifrao(new_preco_produto),
                situacao = new_situacao,
                categoria = new_categoria
            )
            novo_produto.save()

            estoque_novo = Estoque(nome_produto = novo_produto)
            estoque_novo.save()
            return redirect('mostra_produtos')
        
        except Exception as e:
            if 'UNIQUE' in str(e):
                context = {
                    'nome_produto' : new_nome_produto,
                    'codigo_de_barras' : new_codigo_de_barras,
                    'preco_produto' : new_preco_produto,
                    'situacao' : new_situacao,
                    'categoria' : new_categoria
                }
                messages.error(request, 'Código de barras já existe!')
                return render(request, 'cadastro_produtos.html', context)
            else:
                messages.error(request, e)
                return render(request, 'cadastro_produtos.html')
    else:
        categorias = Produto.CATEGORIA_CHOICES
        return render(request, 'cadastro_produtos.html', {'categorias':categorias})

@login_required(login_url='logar')
def EditarProduto(request, produto_id):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    if request.method == 'POST':
        new_nome_produto = request.POST.get('nome_produto')
        new_codigo_de_barras = request.POST.get('codigo_de_barras')
        new_preco_produto = request.POST.get('preco_produto')
        new_preco_produto = new_preco_produto.strip()
        new_preco_produto = new_preco_produto.replace(',', '.')
        new_situacao = True if request.POST.get('situacao') else False

        try:
            
            Produto.objects.filter(id=produto_id).update(
                nome=new_nome_produto,
                codigo_de_barras=new_codigo_de_barras,
                preco=ConverteValorCifrao(new_preco_produto),
                situacao=new_situacao
            )
            return redirect('mostra_produtos')
        except Exception as e:
            if 'UNIQUE' in str(e) and 'codigo_de_barras' in str(e):
                messages.error(request, 'Código de Barras já existe!')
            else:
                messages.error(request, 'Ocorreu um erro ao editar o produto.')
            return redirect('editar_produto', produto_id=produto_id)
    else:
        produtos = Produto.objects.get(id=produto_id)
        produtos.preco = locale.currency(produtos.preco, grouping=True, symbol=True)
        return render(request, 'editar_produto.html', {'produtos': produtos})
    
def ConverteValorCifrao(valor):
    valor = valor.replace('R','').replace('$','').replace(' ','').replace(',' ,'.')
    valor = float(valor)
    return valor
    