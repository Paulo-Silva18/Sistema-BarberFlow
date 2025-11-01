# agendamentos/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.utils import timezone
from .models import Agendamento, Cliente, Barbeiro, Servico # Certifique-se de importar todos os modelos
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Classe personalizada para formatar o campo de data e hora
class CustomDateTimeField(forms.DateTimeField):
    def prepare_value(self, value):
        # Converte o objeto datetime do modelo para o formato da input HTML
        if isinstance(value, timezone.datetime):
            return value.strftime('%Y-%m-%dT%H:%M')
        return super().prepare_value(value)

class AgendamentoForm(forms.ModelForm):
    # Usa a classe personalizada para o campo de data e hora
    data_e_hora = CustomDateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Agendamento
        fields = ['barbeiro', 'servico', 'data_e_hora', 'observacoes']

    def clean_data_e_hora(self):
        data_e_hora = self.cleaned_data.get('data_e_hora')

        # Validação 1: Proíbe agendamentos aos domingos
        if data_e_hora and data_e_hora.weekday() == 6:  # 6 = Domingo
            raise ValidationError("A barbearia não funciona aos domingos. Por favor, escolha outro dia.")

        # Validação 2: Checa se o horário já está ocupado
        if data_e_hora:
            agendamentos_existentes = Agendamento.objects.filter(data_e_hora=data_e_hora)

            if self.instance and self.instance.pk:
                agendamentos_existentes = agendamentos_existentes.exclude(pk=self.instance.pk)
            
            if agendamentos_existentes.exists():
                raise ValidationError("Este horário já está agendado. Por favor, escolha outro horário ou dia.")

        return data_e_hora

class ClienteCreationForm(UserCreationForm):
    telefone = forms.CharField(max_length=20, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
    
    # Sobrescreve o método save para criar o objeto Cliente após o User
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"] # Salva o email
        if commit:
            user.save()
            # Cria e salva o modelo Cliente ligado ao novo User
            cliente = Cliente.objects.create(
                user=user,
                telefone=self.cleaned_data["telefone"]
            )
        return user