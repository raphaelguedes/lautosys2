from django.db import models
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import User


from django.db import models
import datetime

class Conta(models.Model):
	conta_nome = models.CharField(max_length=150)
	def __str__(self):
		return str(self.conta_nome)

class Responsavel(models.Model):
	nome = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	def __str__(self):
		return str(self.nome)

class Unidade(models.Model):
	unidade_nome = models.CharField(max_length=50)
	def __str__(self):
		return str(self.unidade_nome)

class Ccusto(models.Model):
	ccusto_nome = models.CharField(max_length=100)
	unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=True)
	responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, default=1, related_name='responsavel')
	gerente = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


	def __str__(self):
		return str(self.ccusto_nome)

class Meta(models.Model):
	conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
	ccusto = models.ForeignKey(Ccusto, on_delete=models.CASCADE)
	data = models.DateField()
	valor_meta = models.DecimalField(max_digits=8, decimal_places=2)
	chave_meta = models.CharField(max_length=100)

	def __str__(self):
		return '%s %s %s %s %s' % (self.conta, ':',self.data.strftime("%d %m %Y"),':',self.ccusto)

class Despesa(models.Model):
	conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
	ccusto = models.ForeignKey(Ccusto, on_delete=models.CASCADE)
	chave_meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True)
	data = models.DateField()
	valor_despesa = models.DecimalField(max_digits=8, decimal_places=2)
	chave_despesa = models.CharField(max_length=100)

	def __str__(self):
		return str(self.id)

class Alerta(models.Model):
	chave_meta = models.ForeignKey(Meta, on_delete=models.CASCADE, null=True)
	data = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.chave_meta.chave_meta)