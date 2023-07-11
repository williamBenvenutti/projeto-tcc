from django.shortcuts import render, redirect
from .models import Colaborador
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages

@login_required(login_url='logar')
def MostraColabs(request):
    colabs = Colaborador.objects.all()
    quantidade_colabs = Colaborador.objects.count()

    for colab in colabs:
        colab.cpf = mascaraCPF(colab.cpf)

    return render(request, 'mostra_colabs.html', {'colabs':colabs, 'quantidade_colabs':quantidade_colabs})

@login_required(login_url='logar')
def CadastraColabs(request):
    if request.method == 'POST':
        new_nome = request.POST.get('nome')
        new_cpf = request.POST.get('cpf').replace('.', '').replace('-', '')
        new_email = request.POST.get('email')
        new_login = request.POST.get('login')
        new_senha = request.POST.get('senha')
        new_situacao = True if request.POST.get('situacao') else False

        if len(new_cpf) < 11:
            context = {
                'nome': new_nome,
                'cpf': new_cpf,
                'login': new_login,
                'situacao': new_situacao,
                'email' : new_email
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
                situacao=new_situacao
            )
            messages.error(request, 'Colaborador cadastrado!')
            return redirect('mostra_colabs')
        
        except Exception as e:
            if 'cpf' in str(e):
                context = {
                    'nome': new_nome,
                    'cpf': new_cpf,
                    'login': new_login,
                    'situacao': new_situacao,
                    'email' : new_email
                }
                messages.error(request, 'CPF já em uso!')
                return render(request, 'cadastro_colabs.html', context)
            
            elif 'login' in str(e):
                context = {
                    'nome': new_nome,
                    'cpf': new_cpf,
                    'login': new_login,
                    'situacao': new_situacao,
                    'email' : new_email
                }
                messages.error(request, 'Usuario ja em uso!')
                return render(request, 'cadastro_colabs.html', context)
            elif 'email' in str(e):
                context = {
                    'nome': new_nome,
                    'cpf': new_cpf,
                    'login': new_login,
                    'situacao': new_situacao,
                    'email' : new_email
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
        new_situacao = True if request.POST.get('situacao') != None else False

        try:
            Colaborador.objects.filter(id=colab_id).update(
                nome=new_nome,
                cpf=new_cpf,
                login=new_login,
                situacao=new_situacao,
                email=new_email
            )
            messages.error(request, 'Colaborador editado!')
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