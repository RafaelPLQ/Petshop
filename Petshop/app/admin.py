from django.contrib import admin
from .models import (
	Cliente,
	Funcionario,
	Raca,
	Especie,
	Pet,
	Servico,
	Agendamento,
	Pagamento,
)
from django.contrib import admin


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
	list_display = ('id_cliente', 'nome', 'telefone', 'email')


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
	list_display = ('id_funcionario', 'nome', 'telefone', 'email', 'funcao')


@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
	list_display = ('id_raca', 'nome')


@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
	list_display = ('id_especie', 'nome')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
	list_display = ('id_pet', 'nome', 'raca', 'especie', 'idade', 'cliente')
	list_filter = ('raca', 'especie')


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
	list_display = ('id_servico', 'nome', 'valor')


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
	list_display = ('id_agendamento', 'data_agendamento', 'hora', 'pet', 'servico', 'funcionario')
	list_filter = ('data_agendamento', 'servico')


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
	list_display = ('id_pagamento', 'agendamento', 'valor', 'forma_pagamento', 'data_pagamento')    
