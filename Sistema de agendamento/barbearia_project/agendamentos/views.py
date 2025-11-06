# agendamentos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .forms import AgendamentoForm, ClienteCreationForm 
from .models import Agendamento, Cliente 

from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.forms import AuthenticationForm

@login_required
def agendar_corte(request):
    # Tenta pegar o objeto Cliente ligado ao User logado
    try:
        cliente_logado = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, 'Erro: Seu perfil de cliente não está completo.')
        return redirect('logout') # Força o logout se o perfil estiver incompleto

    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            # 1. Preenche o campo cliente automaticamente com o usuário logado
            agendamento.cliente = cliente_logado
            agendamento.save()
            
            messages.success(request, 'Agendamento realizado com sucesso!')
            return redirect('agendar_corte')
    else:
        form = AgendamentoForm()
    
    return render(request, 'agendamentos/agendar.html', {'form': form})

def lista_agendamentos(request):
    # Filtra por agendamentos futuros e ordena por data e hora
    agendamentos = Agendamento.objects.filter(data_e_hora__gte=timezone.now()).order_by('data_e_hora')

    return render(request, 'agendamentos/lista_agendamentos.html', {'agendamentos': agendamentos})

@login_required
def editar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect('lista_agendamentos')  # Redireciona para a lista após a edição
    else:
        form = AgendamentoForm(instance=agendamento)

    return render(request, 'agendamentos/editar_agendamento.html', {'form': form})

def deletar_agendamento(request, pk):
    # Encontra o agendamento a ser deletado ou retorna 404
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    # O método de deleção deve ser POST para segurança
    if request.method == 'POST':
        agendamento.delete()
        messages.success(request, 'Agendamento excluído com sucesso!')
        return redirect('lista_agendamentos') # Redireciona para a lista após a exclusão
    
    # Se a requisição não for POST, redireciona para a lista
    return redirect('lista_agendamentos')

def cadastro_cliente(request):
    if request.method == 'POST':
        form = ClienteCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Loga o usuário imediatamente após o cadastro
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso! Você está logado.')
            return redirect('agendar_corte') # Redireciona para o agendamento
        else:
            # Exibe erros de validação do formulário de cadastro
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
            
    else:
        form = ClienteCreationForm()
    
    return render(request, 'agendamentos/cadastro.html', {'form': form})


# NOVO VIEW: Login (RF02)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Login efetuado com sucesso! Olá, {username}.')
                return redirect('agendar_corte')
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    
    form = AuthenticationForm()
    return render(request, 'agendamentos/login.html', {'form': form})

# NOVO VIEW: Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('agendar_corte')