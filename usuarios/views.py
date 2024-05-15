from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

def Cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/pacientes/home")
        
        return render(request, 'cadastro.html')
    
    elif request.method == "POST":
        nome_completo = request.POST.get('nome_completo')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if not email or not senha or not nome_completo:
            messages.add_message(request, constants.ERROR, "Por favor, preencha todos os campos.")
            return redirect("/usuarios/cadastro")
        
        confirmar_senha = request.POST.get('confirmar_senha')
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, "A senha e o confirmar senha devem ser iguais.")
            return redirect('/usuarios/cadastro')
        
        elif len(senha) < 6:
            messages.add_message(request, constants.ERROR, "A senha deve ter mais de 6 dígitos.")
            return redirect('/usuarios/cadastro')
        
        nome_dividido = nome_completo.split()
        primeiro_nome = nome_dividido[0]
        sobrenome = " ".join(nome_dividido[1:])
        
        users = User.objects.filter(email=email)
        if users.exists():
            messages.add_message(request, constants.ERROR, "Já existe um usuário com esse e-mail.")
            return redirect('/usuarios/cadastro')
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=primeiro_nome,
            last_name=sobrenome
        )
        
        return redirect('/usuarios/login')

def Login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/pacientes/home")
        
        return render(request, "login.html")
    
    elif request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if not email or not senha:
            messages.add_message(request, constants.ERROR, "Por favor, informe um e-mail e senha para login.")
            return redirect("/usuarios/login")
        
        try:
            user = auth.authenticate(request, username=User.objects.get(email=email).username, password=senha)
        except:
            messages.add_message(request, constants.ERROR, "E-mail ou senha inválidos.")
            return redirect("/usuarios/login")
        
        if user:
            auth.login(request, user)
            return redirect("/pacientes/home")
        
        messages.add_message(request, constants.ERROR, "E-mail ou senha inválidos.")
        return redirect("/usuarios/login")

@login_required
def Logout(request):
    auth.logout(request)
    return redirect('/usuarios/login')