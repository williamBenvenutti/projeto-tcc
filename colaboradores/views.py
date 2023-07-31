from django.shortcuts import render, redirect
from .models import Colaborador
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages

@login_required(login_url='logar')
def MostraColabs(request):
    if request.method == 'GET':
        filtro_nome = request.GET.get('filtro_nome', None)
        filtro_email = request.GET.get('filtro_email', None)
        filtro_cpf = request.GET.get('filtro_cpf', None)
        filtro_situacao = request.GET.get('filtro_situacao', None)
        
        colabs = Colaborador.objects.all()

        if filtro_nome:
            colabs = Colaborador.objects.filter(nome__icontains=filtro_nome)

        if filtro_email:
            colabs = Colaborador.objects.filter(email__icontains=filtro_email)

        if filtro_cpf:
            filtro_cpf = filtro_cpf.replace('.','').replace('-','')
            colabs = Colaborador.objects.filter(cpf__icontains=filtro_cpf)

        if filtro_situacao:
            if filtro_situacao == 'ativo':
                colabs = colabs.filter(situacao=True)
            elif filtro_situacao == 'inativo':
                colabs = colabs.filter(situacao=False)

        colabs = colabs.order_by('-situacao','nome')

        for colab in colabs:
            colab.cpf = mascaraCPF(colab.cpf)

        return render(request, 'mostra_colabs.html', {'colabs':colabs})

@login_required(login_url='logar')
def CadastraColabs(request):
    if request.method == 'POST':
        new_nome = request.POST.get('nome')
        new_cpf = request.POST.get('cpf').replace('.', '').replace('-', '')
        new_email = request.POST.get('email')
        new_login = request.POST.get('login')
        new_codigo_de_barras = request.POST.get('codigo_de_barras')

        new_senha = GerarSenha(new_cpf, new_login)
        print(new_senha)

        new_situacao = True if request.POST.get('situacao') else False

        if len(new_cpf) < 11:
            context = {
                'nome': new_nome,
                'cpf': new_cpf,
                'login': new_login,
                'situacao': new_situacao,
                'email' : new_email,
                'codigo_de_barras' : new_codigo_de_barras
            }
            
            messages.error(request, 'CPF Inválido!')
            return render(request, 'cadastro_colabs.html', context)

        try:
            senha_criptografada = make_password(new_senha)
            Colaborador.objects.create(
                nome=new_nome,
                cpf=new_cpf,
                email=new_email,
                login=new_login,
                senha=senha_criptografada,
                situacao=new_situacao,
                codigo_de_barras = new_codigo_de_barras
            )
            return redirect('mostra_colabs')
        
        except Exception as e:
            if 'cpf' in str(e):
                context = {
                    'nome': new_nome,
                    'cpf': new_cpf,
                    'login': new_login,
                    'situacao': new_situacao,
                    'email' : new_email,
                    'codigo_de_barras' : new_codigo_de_barras
                }
                messages.error(request, 'CPF já em uso!')
                return render(request, 'cadastro_colabs.html', context)
            
            elif 'login' in str(e):
                context = {
                    'nome': new_nome,
                    'cpf': new_cpf,
                    'login': new_login,
                    'situacao': new_situacao,
                    'email' : new_email,
                    'codigo_de_barras' : new_codigo_de_barras
                }
                messages.error(request, 'Usuario ja em uso!')
                return render(request, 'cadastro_colabs.html', context)
            elif 'email' in str(e):
                context = {
                    'nome': new_nome,
                    'cpf': new_cpf,
                    'login': new_login,
                    'situacao': new_situacao,
                    'email' : new_email,
                    'codigo_de_barras' : new_codigo_de_barras
                }
                messages.error(request, 'Email ja em uso!')
                return render(request, 'cadastro_colabs.html', context)
            else:
                return HttpResponse(e)
    else:
        return render(request, 'cadastro_colabs.html')

@login_required(login_url='logar')
def EditarColab(request, colab_id):
    if request.method == 'POST':
        new_nome = request.POST.get('nome')
        new_cpf = request.POST.get('cpf')
        new_cpf = new_cpf.replace('.', '').replace('-', '')
        new_email = request.POST.get('email')
        new_login = request.POST.get('login')
        new_codigo_de_barras = request.POST.get('codigo_de_barras')
        new_situacao = True if request.POST.get('situacao') != None else False

        try:
            Colaborador.objects.filter(id=colab_id).update(
                nome=new_nome,
                cpf=new_cpf,
                login=new_login,
                situacao=new_situacao,
                email=new_email,
                codigo_de_barras=new_codigo_de_barras
            )
            return redirect('mostra_colabs')
        
        except Exception as e:
            if 'cpf' in str(e):
                messages.error(request,'CPF já em uso')
                return render(request, 'editar_colab.html', {'colab': colab})
            
            elif 'login' in str(e):
                messages.error(request,'Login ja em uso!')
                return render(request, 'editar_colab.html', {'colab': colab})
            elif 'email' in str(e):
                messages.error(request, 'Email ja em uso!')
                return render(request, 'editar_colab.html', {'colab': colab})
            else:
                return HttpResponse(e)
            
    else:
        colab = Colaborador.objects.get(id = colab_id)
        colab.cpf = mascaraCPF(colab.cpf)
        return render(request, 'editar_colab.html', {'colab': colab, 'colab.cpf':colab.cpf})
        
def mascaraCPF(cpf):
    cpf = str(cpf)
    cpf_formatado = "{}.{}.{}-{}".format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
    return cpf_formatado


# def validaCpf(cpf):
#     if cpf == cpf[0] * 11:
#         return False
#     soma = 0
#     for i in range(9):
#         soma += int(cpf[i]) * (10 - i)

#     primeiro_digito = 11 - (soma % 11)

#     if primeiro_digito > 9:
#         primeiro_digito = 0

#     soma = 0
#     for i in range(10):
#         soma += int(cpf[i]) * (11 - i)
#     segundo_digito = 11 - (soma % 11)
#     if segundo_digito > 9:
#         segundo_digito = 0

#     if int(cpf[-2]) == primeiro_digito and int(cpf[-1]) == segundo_digito:
#         return True
#     else:
#         return False
    
def GerarSenha(cpf, login):
    nova_senha = ''

    for digito in login:
        if digito == '.':
            break
        else:
            nova_senha += digito
    
    nova_senha += cpf[:3]
    
    return nova_senha
