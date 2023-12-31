from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from estoque.models import Estoque
from compras.models import RegistroCompra
from colaboradores.models import Colaborador
from datetime import datetime, timedelta, date

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciais inválidas!')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required(login_url='logar')
def Dashboard(request):
    data_atual = datetime.now().date()
    estoque = Estoque.objects.filter(quantidade__lte=6, nome_produto__categoria="alimento", nome_produto__situacao=True)
    qtd_estoque = (estoque.count()) - 4
    print(qtd_estoque)
    estoque = estoque.order_by('quantidade')[:4]

    compras = RegistroCompra.objects.filter(data_compra__date=data_atual).order_by('-data_compra')[:5]
    colabs = Colaborador.objects.filter(situacao = True)
    colabs = colabs.order_by('nome')[:5]

    context = {
        'estoque': estoque,
        'compras': compras,
        'qtd_estoque' : qtd_estoque,
        'colabs' : colabs
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='logar')
def CadastroUsuario(request):
    if not request.user.is_superuser:
        return HttpResponse("Acesso negado.")
    else:
        if request.method == 'POST':
            try:
                new_first_name = request.POST.get('first_name')
                new_last_name = request.POST.get('last_name')
                new_username = request.POST.get('username')
                new_password = request.POST.get('password')
                new_email = request.POST.get('email')
                
                user = User.objects.create(
                    first_name=new_first_name,
                    last_name=new_last_name,
                    username=new_username,
                    email=new_email
                )
                user.set_password(new_password)
                user.save()
                
                return redirect('mostra_usuario')
            except Exception as e:
                if 'UNIQUE' in str(e) and "username" in str(e):
                    context = {
                        'first_name' : new_first_name,
                        'last_name' : new_last_name,
                        'username' : new_username,
                        'email' : new_email
                    }
                    messages.error(request, 'Usuario ja existe!')
                    return render(request, 'cadastra_usuario.html', context)
                
                elif 'UNIQUE' in str(e) and 'email' in str(e):
                    context = {
                        'first_name' : new_first_name,
                        'last_name' : new_last_name,
                        'username' : new_username,
                        'email' : new_email
                    }
                    messages.error(request, 'Email ja existe!')
                    return render(request, 'cadastra_usuario.html', context)
                else:
                    return HttpResponse(e)
        else:
            return render(request, 'cadastra_usuario.html')

        
@login_required(login_url='logar')
def MostraUsuario(request):
    if request.method == 'GET':
        filtro_nome = request.GET.get('filtro_nome', None)
        filtro_sobrenome = request.GET.get('filtro_sobrenome', None)
        filtro_email = request.GET.get('filtro_email', None)

        print(filtro_nome)

        users = User.objects.all()

        if filtro_nome:
            users = users.filter(first_name__icontains=filtro_nome)

        if filtro_sobrenome:
            users = users.filter(last_name__icontains=filtro_sobrenome)

        if filtro_email:
            users = users.filter(email__icontains=filtro_email)

        print(users)

        return render(request, 'mostra_usuarios.html', {'users':users})

@login_required(login_url='logar')
def EditarUsuario(request, user_id):

    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado!')
        return redirect('dashboard')
    else:
        try:
            users = User.objects.get(id = user_id)
        except:
            messages.error(request, 'Usuario nao encontrado!')
            return redirect('mostra_usuario')

        if request.method == 'POST':
            new_first_name = request.POST.get('first_name')
            new_last_name = request.POST.get('last_name')
            new_username = request.POST.get('username')
            new_email = request.POST.get('email')

            try:
                User.objects.filter(id = user_id).update(
                    first_name = new_first_name,
                    last_name = new_last_name,
                    username = new_username,
                    email = new_email
                )
                return redirect('mostra_usuario')
            except Exception as e:
                if 'username' in str(e):
                    messages.error(request, 'Usuario ja existe!')
                    return redirect('editar_usuario', user_id = user_id)
                elif 'email' in str(e):
                    messages.error(request, 'Email ja existe!')
                    return redirect('editar_usuario', user_id = user_id)
        else:
            return render(request, 'editar_usuario.html', {'users':users})
        
def AlteraSenha(request, user_id):
    users = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        nova_senha = request.POST.get('senha')
        valida_senha = request.POST.get('valida_senha')
        users.set_password(nova_senha)
        users.save()
        return redirect('editar_usuario', user_id = user_id)
    
 
def ExcluiUsuario(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso negado!')
        return redirect('dashboard')
    else:
        try:
            User.objects.filter(id=user_id).delete()
            return redirect('mostra_usuario')
        except:
            messages.error(request, 'Usuário não pode ser deletado!')
            return redirect('editar_usuario', user_id = user_id)

def Logout(request):
    logout(request)
    return redirect('logar')


