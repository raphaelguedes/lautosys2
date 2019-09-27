from django.db import models
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import User

from django.db import models
import datetime

from gmcdalert.models import Ccusto

###################################################################################################################

class Tipouser(models.Model):
	tipo_user = models.CharField(max_length=30)

	def __str__(self):
		return self.tipo_user

class Setor(models.Model):
	nome_setor = models.CharField(max_length=30)
	ccusto = models.ForeignKey(Ccusto, on_delete=models.CASCADE, default = 157)

	def __str__(self):
		return self.nome_setor

class Cargo(models.Model):
	nome_cargo = models.CharField(max_length=50)

	def __str__(self):
		return self.nome_cargo

class Modulo(models.Model):
	nome_modulo = models.CharField(max_length=30)

	def __str__(self):
		return self.nome_modulo

class Acesso(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.usuario.first_name

class User2(models.Model):
	tipo_user = models.ForeignKey(Tipouser, on_delete=models.CASCADE, default = 1)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	matricula = models.CharField(max_length=6, null=True, blank=True, default = 0)
	nome = models.CharField(max_length=50, null=True, blank=True)
	cpf = models.CharField(max_length=15)
	telefone_1 = models.CharField(max_length=15, null=True, blank=True)
	telefone_2 = models.CharField(max_length=15, null=True, blank=True)
	datan = models.DateField(null=True, blank=True)
	setor = models.ForeignKey(Setor, on_delete=models.CASCADE, default = 1)
	cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, default = 1)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.nome

class Classe(models.Model):
	nome_classe = models.CharField(max_length=30)

	def __str__(self):
		return self.nome_classe

class Tipoveiculo(models.Model):
	tipo_veiculo = models.CharField(max_length=30)

	def __str__(self):
		return self.tipo_veiculo

class Marca(models.Model):
	marca_veiculo = models.CharField(max_length=50)

	def __str__(self):
		return self.marca_veiculo

class Modelo(models.Model):
	modelo_veiculo = models.CharField(max_length=50)

	def __str__(self):
		return self.modelo_veiculo

class Veiculos(models.Model):
	placa = models.CharField(max_length=15)
	setor = models.ForeignKey(Setor, on_delete=models.CASCADE, default = 1)
	marca = models.ForeignKey(Marca, on_delete=models.CASCADE, default = 1)
	modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, default = 1)
	tipo = models.ForeignKey(Tipoveiculo, on_delete=models.CASCADE, default = 1)
	classe = models.ForeignKey(Classe, on_delete=models.CASCADE, default = 1)
	status = models.BooleanField(default=True)

	
	def __str__(self):
		return self.placa

#	def __str__(self):
#		return '%s %s %s %s' % (self.usuario.first_name, self.usuario.last_name , ':' , self.nome_contratante)
####################################################################################################################