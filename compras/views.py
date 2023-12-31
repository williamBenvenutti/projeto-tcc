from django.shortcuts import render, redirect
from colaboradores.models import Colaborador
from estoque.models import Estoque
from produtos.models import Produto
from .models import RegistroCompra, ItemCompra
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum, F
from django.contrib.auth.hashers import check_password
from django.contrib import messages
import locale
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from weasyprint import HTML
import cv2
from pyzbar.pyzbar import decode

carrinho = list()

def TelaCompra(request):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    if request.method == 'POST':
        codigo_de_barras_digitado = LeituraCodigoBarras()
        produto = Produto.objects.filter(codigo_de_barras=codigo_de_barras_digitado).first()

        if produto is None or produto.situacao == False:
            messages.error(request, 'Produto não encontrado!')
            return redirect('realizar_compras')
        else:
            quantidade_carrinho = CalculaQuantidadeCarrinho(produto, carrinho)
            quantidade_estoque = Estoque.objects.get(nome_produto=produto)
            produto.nome = produto.nome[:17]
            produto.nome += '.'
            print(produto.nome)
            if quantidade_carrinho < quantidade_estoque.quantidade:
                carrinho.append(produto)
                soma_precos = sum(produto.preco for produto in carrinho)
                soma_precos = round(soma_precos, 2)
            else:
                messages.error(request, 'Estoque Esgotado')
                return redirect('realizar_compras')

        return redirect('realizar_compras')
    else:
        soma_precos = sum(produto.preco for produto in carrinho)
        soma_precos_formatted = locale.currency(soma_precos, grouping=True, symbol=True)
        print(soma_precos_formatted)

        context = {
            'soma_precos' : soma_precos,
            'soma_precos_formatted' : soma_precos_formatted,
            'carrinho' : carrinho
        }

        return render(request, "tela_compra.html", context)

def RemoverProduto(request, index):
    carrinho.pop(index - 1)
    return redirect('realizar_compras')

def LimpaCarrinho(request):
    carrinho.clear()
    return redirect('realizar_compras')

def FinalizaCompra(request):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    data_limite = verificaData()
    
    if request.method == 'GET':
        if not carrinho:
            messages.error(request, 'Carrinho vazio!')
            return redirect('realizar_compras')
        
        codigo_colaborador = LeituraCodigoBarras()
        print(codigo_colaborador)
        colaborador = Colaborador.objects.filter(codigo_de_barras=codigo_colaborador).first()

        if colaborador is None:
            messages.error(request, 'Usuario não encontrado!')
            return redirect('realizar_compras')
        
        elif colaborador.situacao == False:
            messages.error(request, 'Colaborador Inativo!')
            return redirect('realizar_compras')
        
        else:
            compra = RegistroCompra.objects.create(colab_id=colaborador, data_compra=datetime.now())

            itens_compra = []
            quantidade_produtos = {}

            for produto in carrinho:
                if produto in quantidade_produtos:
                    quantidade_produtos[produto] += 1
                else:
                    quantidade_produtos[produto] = 1

            for produto, quantidade in quantidade_produtos.items():
                item = ItemCompra(compra=compra, produto=produto, quantidade=quantidade, preco_individual=produto.preco)
                itens_compra.append(item)
                
                if produto.categoria != 'cinema' and produto.categoria != 'vestuario':
                    estoque = Estoque.objects.get(nome_produto=produto)
                    estoque.quantidade -= quantidade
                    estoque.save()

                if produto.categoria == 'cinema':
                    EnviarEmailIngresso(colaborador, produto, quantidade)
                elif produto.categoria == 'vestuario':
                    EnviarEmailCamisa(colaborador, produto, quantidade)

            ItemCompra.objects.bulk_create(itens_compra)

            final_compra = sum(produto.preco for produto in carrinho)
            final_compra = locale.currency(final_compra, grouping=True)

            EnviarEmail(colaborador, carrinho, final_compra)

            total = calculaTotalCompras(colaborador, data_limite)
            total_anterior = calculaTotalComprasReferenciaAnterior(colaborador)
            carrinho.clear()

            return render(request, 'tela_compra.html', {'total':total, 'carrinho':carrinho, 'total_anterior':total_anterior})


def MostraTotalGasto(request):
    if request.method == 'GET':
        codigo_colaborador = LeituraCodigoBarras()
        
        colaborador = Colaborador.objects.filter(codigo_de_barras=codigo_colaborador).first()

        if colaborador is None:
            messages.error(request, 'Usuario não encontrado!')
            return redirect('realizar_compras')
        
        elif colaborador.situacao == False:
            messages.error(request, 'Colaborador Inativo!')
            return redirect('realizar_compras')
        else:
            data_limite = verificaData()

            total = calculaTotalCompras(colaborador, data_limite)
            total_anterior = calculaTotalComprasReferenciaAnterior(colaborador)
            print(total)
            print(total_anterior)
            return render(request, 'tela_compra.html', {'total':total, 'carrinho':carrinho, 'total_anterior':total_anterior})
    else:
        return redirect('realizar_compras')

def verificaData():
    data_atual = datetime.now().date()
    dia_atual = data_atual.day

    if dia_atual <= 25:
        if data_atual.month == 1:
            data_limite = datetime(data_atual.year - 1, 12, 26).date()
        else:
            data_limite = datetime(data_atual.year, data_atual.month - 1, 26).date()
    else:
        data_limite = datetime(data_atual.year, data_atual.month, 26).date()

    return data_limite

def calculaTotalCompras(colaborador, data_limite):
    total = RegistroCompra.objects.filter(
        colab_id=colaborador,
        data_compra__gte=data_limite
    ).aggregate(total_compras=Sum(F('itemcompra__preco_individual') * F('itemcompra__quantidade')))['total_compras']

    if total is not None and total > 0:
        return round(total, 2)
    else:
        return 0.0
    
def calculaTotalComprasReferenciaAnterior(colaborador):
    data_atual = datetime.now().date()
    data_limite = verificaData()
    mes_atual = data_atual.month
    ano_atual = data_atual.year
    if mes_atual == 1:
        mes_anterior = 12
        ano_anterior = ano_atual - 1
    else:
        mes_anterior = mes_atual - 1
        ano_anterior = ano_atual
        
    if mes_anterior == data_limite.month:
        mes_anterior -=1
        mes_atual -=1

    data_inicio = datetime(ano_anterior, mes_anterior, 26).date()
    data_fim = datetime(ano_atual, mes_atual, 25).date()

    total = RegistroCompra.objects.filter(
        colab_id=colaborador,
        data_compra__range=(data_inicio, data_fim)
    ).aggregate(total_compras=Sum(F('itemcompra__preco_individual') * F('itemcompra__quantidade')))['total_compras']

    if total is not None and total > 0:
        return round(total, 2)
    else:
        return 0.0
    
def EnviarEmail(colab, carrinho, final_compra):
    data_atual = datetime.now()
    subject = 'Compra realizada na Conveniência SCI'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [colab.email]

    context = {
        'carrinho':carrinho,
        'colaborador':colab,
        'final_compra':final_compra
    }

    mensagem_html = render_to_string('padrao_email.html', context)
    anexo_email = render_to_string('anexo_email.html', context)

    pdf_bytes = HTML(string=anexo_email).write_pdf()

    anexo_email = EmailMultiAlternatives(
        subject = subject,
        from_email = from_email,
        to = recipient_list
    )

    anexo_email.attach_alternative(mensagem_html, 'text/html')

    anexo_email.attach(f'Comprovante de compra-{data_atual}', pdf_bytes,'application/pdf')

    anexo_email.send()


def EnviarEmailIngresso(colab, produto, quantidade):
    subject = 'Compra de ingresso realizada na Conveniência SCI'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['benvenuttiwilliam@gmail.com']

    context = {
        'produto':produto,
        'colaborador':colab,
        'quantidade':quantidade
    }

    nome_template = 'email_ingresso.html'
    mensagem_html = render_to_string(nome_template, context)
    plain_message = strip_tags(mensagem_html)

    send_mail(subject, plain_message, from_email, recipient_list, html_message=mensagem_html)

def EnviarEmailCamisa(colab, produto, quantidade):
    subject = 'Compra de camisa realizada na Conveniência SCI'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['benvenuttiwilliam@gmail.com']

    context = {
        'produto':produto,
        'colaborador':colab,
        'quantidade':quantidade
    }

    nome_template = 'email_camisa.html'
    mensagem_html = render_to_string(nome_template, context)
    plain_message = strip_tags(mensagem_html)

    send_mail(subject, plain_message, from_email, recipient_list, html_message=mensagem_html)

def CalculaQuantidadeCarrinho(produto, carrinho):
    quantidade = 0
    for item in carrinho:
        if produto == item:
            quantidade+=1
    return quantidade

def LeituraCodigoBarras():
    cap = cv2.VideoCapture(0)
    cap.set(3, 840)
    cap.set(4, 480)
    camera = True
    codigo_de_barras = ''
    while camera:
        sucess, frame = cap.read()
        for code in decode(frame):
            codigo_de_barras = code.data.decode('utf-8')
            print(codigo_de_barras)
            camera = False 
        if sucess:
            cv2.imshow('Testando leitor de codigo de barras', frame)
            cv2.waitKey(1)
    cv2.destroyAllWindows()
    print(codigo_de_barras)
    return codigo_de_barras