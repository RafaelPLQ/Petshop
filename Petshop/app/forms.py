import django.forms as forms
from app.models import *
from django.contrib.auth.models import User



class RacaFormView(forms.ModelForm):
    class Meta:
        model = Raca
        fields = ['nome']
        labels = {
            'nome': 'Nome da Raça'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da raça'
            })
        }


class EspecieFormView(forms.ModelForm):
    class Meta:
        model = Especie
        fields = ['nome']
        labels = {
            'nome': 'Nome da Espécie'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da espécie'
            })
        }


class FuncionarioFormView(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'telefone', 'email', 'funcao']
        labels = {
            'nome': 'Nome do Funcionário',
            'telefone': 'Telefone',
            'email': 'Email',
            'funcao': 'Função'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do funcionário'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o telefone'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o email'
            }),
            'funcao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a função'
            })
        }


class ServicoFormView(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'valor']
        labels = {
            'nome': 'Nome do Serviço',
            'valor': 'Valor'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do serviço'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            })
        }


class PetFormView(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['nome', 'raca', 'especie', 'idade', 'cliente']
        labels = {
            'nome': 'Nome do Pet',
            'raca': 'Raça',
            'especie': 'Espécie',
            'idade': 'Idade',
            'cliente': 'Cliente'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do pet'
            }),
            'raca': forms.Select(attrs={
                'class': 'form-select'
            }),
            'especie': forms.Select(attrs={
                'class': 'form-select'
            }),
            'idade': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Idade em anos'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class AgendamentoFormView(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['data_agendamento', 'hora', 'descricao', 'pet', 'servico']
        labels = {
            'data_agendamento': 'Data',
            'hora': 'Hora',
            'descricao': 'Descrição',
            'pet': 'Pet',
            'servico': 'Serviço'
        }
        widgets = {
            'data_agendamento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hora': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição (opcional)'
            }),
            'pet': forms.Select(attrs={
                'class': 'form-select'
            }),
            'servico': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Clientes só veem seus próprios pets
        if user and not getattr(user, 'is_staff', False):
            self.fields['pet'].queryset = Pet.objects.filter(cliente__email=user.email).order_by('nome')
        else:
            self.fields['pet'].queryset = Pet.objects.all().order_by('nome')

        # Ordenar serviços por nome
        self.fields['servico'].queryset = Servico.objects.all().order_by('nome')
        # Não expor funcionário no formulário (será atribuído automaticamente)

    def clean(self):
        cleaned = super().clean()
        pet = cleaned.get('pet')
        data = cleaned.get('data_agendamento')
        hora = cleaned.get('hora')
        # Impedir double-booking do pet
        if pet and data and hora:
            qs = Agendamento.objects.filter(pet=pet, data_agendamento=data, hora=hora)
            if self.instance and getattr(self.instance, 'id_agendamento', None):
                qs = qs.exclude(id_agendamento=self.instance.id_agendamento)
            if qs.exists():
                raise forms.ValidationError('Este pet já tem um agendamento nesse horário.')

        return cleaned
