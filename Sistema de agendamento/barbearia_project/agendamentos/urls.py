# agendamentos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URLs de AUTENTICAÇÃO
    path('cadastro/', views.cadastro_cliente, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # URLs de AGENDAMENTO
    path('', views.agendar_corte, name='agendar_corte'),
    path('lista-agendamentos/', views.lista_agendamentos, name='lista_agendamentos'),
    path('editar/<int:pk>/', views.editar_agendamento, name='editar_agendamento'),
    path('deletar/<int:pk>/', views.deletar_agendamento, name='deletar_agendamento'),
]