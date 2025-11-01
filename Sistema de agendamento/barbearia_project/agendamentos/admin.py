# agendamentos/admin.py
from django.contrib import admin
from .models import Barbeiro, Servico, Cliente, Agendamento

admin.site.register(Barbeiro)
admin.site.register(Servico)
admin.site.register(Cliente)
admin.site.register(Agendamento)