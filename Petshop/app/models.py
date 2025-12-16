from django.db import models


class Cliente(models.Model):
	id_cliente = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=100)
	telefone = models.CharField(max_length=20, blank=True, null=True)
	email = models.CharField(max_length=100, blank=True, null=True)
	endedeco = models.CharField(max_length=150, blank=True, null=True)

	class Meta:
		db_table = 'cliente'

	def __str__(self):
		return self.nome


class Funcionario(models.Model):
	id_funcionario = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=100)
	telefone = models.CharField(max_length=20, blank=True, null=True)
	email = models.CharField(max_length=100, blank=True, null=True)
	funcao = models.CharField(max_length=150, blank=True, null=True)

	class Meta:
		db_table = 'funcionario'

	def __str__(self):
		return self.nome


class Raca(models.Model):
	id_raca = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=45)

	class Meta:
		db_table = 'raca'

	def __str__(self):
		return self.nome


class Especie(models.Model):
	id_especie = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=45)

	class Meta:
		db_table = 'especie'

	def __str__(self):
		return self.nome


class Pet(models.Model):
	id_pet = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=45)
	raca = models.ForeignKey(Raca, db_column='id_raca', on_delete=models.CASCADE, related_name='pets')
	especie = models.ForeignKey(Especie, db_column='id_especie', on_delete=models.CASCADE, related_name='pets')
	idade = models.IntegerField(blank=True, null=True)
	cliente = models.ForeignKey(Cliente, db_column='id_cliente', on_delete=models.CASCADE, related_name='pets')

	class Meta:
		db_table = 'pet'

	def __str__(self):
		return self.nome


class Servico(models.Model):
	id_servico = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=45)
	valor = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		db_table = 'servico'

	def __str__(self):
		return self.nome


class Agendamento(models.Model):
	id_agendamento = models.AutoField(primary_key=True)
	data_agendamento = models.DateField()
	hora = models.TimeField()
	descricao = models.CharField(max_length=45, blank=True, null=True)
	pet = models.ForeignKey(Pet, db_column='id_pet', on_delete=models.CASCADE, related_name='agendamentos')
	servico = models.ForeignKey(Servico, db_column='id_servico', on_delete=models.CASCADE, related_name='agendamentos')
	funcionario = models.ForeignKey(Funcionario, db_column='id_funcionario', on_delete=models.CASCADE, related_name='agendamentos')

	class Meta:
		db_table = 'agendamento'

	def __str__(self):
		return f"{self.data_agendamento} {self.hora} - {self.pet}"


class Pagamento(models.Model):
	id_pagamento = models.AutoField(primary_key=True)
	agendamento = models.ForeignKey(Agendamento, db_column='id_agendamento', on_delete=models.CASCADE, related_name='pagamentos')
	valor = models.DecimalField(max_digits=10, decimal_places=2)
	forma_pagamento = models.CharField(max_length=20, blank=True, null=True)
	data_pagamento = models.DateTimeField(blank=True, null=True)

	class Meta:
		db_table = 'pagamento'

	def __str__(self):
		return f"Pagamento {self.id_pagamento} - {self.valor}"
