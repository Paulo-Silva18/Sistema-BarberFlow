# agendamentos/models.py

from django.db import models
from django.contrib.auth.models import User 

class Barbeiro(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        # Retorna o nome de usuário do objeto User ligado.
        return self.user.username 

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    duracao_minutos = models.IntegerField(default=30)
    
    def __str__(self):
        return f'{self.nome} (R${self.preco})'

class Agendamento(models.Model):
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    ) 

    # RELACIONAMENTO 2: BARBEIRO
    barbeiro = models.ForeignKey(
        Barbeiro, 
        on_delete=models.CASCADE,
    )
    
    servico = models.ForeignKey(
        Servico, 
        on_delete=models.PROTECT # Usar PROTECT evita deletar um serviço se ele tiver agendamentos ligados.
    )
    data_e_hora = models.DateTimeField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        # Ajusta a representação para usar o barbeiro e o serviço
        return f'{self.barbeiro.nome} - {self.servico.nome} em {self.data_e_hora.strftime("%d/%m/%Y %H:%M")}'