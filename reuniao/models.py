from django.db import models
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import User

from django.db import models
import datetime

class Status_r(models.Model):
	status_r = models.CharField(max_length=20, default=1)
	def __str__(self):
		return str(self.status_r)

class Tipo_r(models.Model):
	tipo = models.CharField(max_length=20)
	def __str__(self):
		return str(self.tipo)

class Tipo_acesso(models.Model):
	tipo_acesso = models.CharField(max_length=20)
	def __str__(self):
		return str(self.tipo_acesso)

class Reuniao(models.Model):
	titulo = models.CharField(max_length=250)
	assunto = models.CharField(max_length=300,null=True, blank=True)
	data = models.DateTimeField(default=timezone.now)
	pauta = models.CharField(max_length=400, null=True, blank=True)
	tipo_reuniao = models.ForeignKey(Tipo_r, on_delete=models.CASCADE)
	status_r = models.ForeignKey(Status_r, on_delete=models.CASCADE)

	def __str__(self):
	#	return str(self.data.strftime("%d %m %Y-%H:%M:%S"))
		return '%s %s %s' % (self.titulo, ':',self.data.strftime("%d %m %Y-%H:%M:%S"))

class Acesso_r(models.Model):
	participante = models.ForeignKey(User, on_delete=models.CASCADE)
	reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE)
	tipo_acesso = models.ForeignKey(Tipo_acesso, on_delete=models.CASCADE, default=1)
	status  = models.BooleanField(default=True)
	def __str__(self):
		return '%s %s %s' % (self.participante, ':',self.reuniao.titulo)

class Area(models.Model):
	nome_area = models.CharField(max_length=40)
	def __str__(self):
		return str(self.nome_area)

class Indicador(models.Model):
	indicador = models.CharField(max_length=40)
	def __str__(self):
		return str(self.indicador)

class Status(models.Model):
	status = models.CharField(max_length=40)
	def __str__(self):
		return str(self.status)

class Planoacao(models.Model):
	nome = models.CharField(max_length=400)
	reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE)
	def __str__(self):
		return '%s %s %s' % (self.nome, ':',self.reuniao)

class Acao(models.Model):
	responsavel = models.ForeignKey(User, on_delete=models.CASCADE)
	planoacao = models.ForeignKey(Planoacao, on_delete=models.CASCADE)
	reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE)
	data_i = models.DateTimeField(default=timezone.now)
	data_start_acao = models.DateTimeField(null=True, blank=True)
	data_conclusao_acao = models.DateTimeField(null=True, blank=True)
	data_inicioprevisto = models.DateTimeField(default=timezone.now)
	prazo = models.DateTimeField(default=timezone.now)
	objetivo = models.CharField(max_length=400)
	motivo = models.CharField(max_length=400, null=True, blank=True)
	custo = models.CharField(max_length=200, null=True, blank=True)
	atividade = models.CharField(max_length=400, null=True, blank=True)
	area = models.ForeignKey(Area, on_delete=models.CASCADE)
	status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)

	def __str__(self):
		return '%s %s %s' % (self.id, ':',self.objetivo)

class Comentario2(models.Model):
	conteudo = models.CharField(max_length=300)
	data_c = models.DateTimeField(default=timezone.now)
	acao_c = models.ForeignKey(Acao, on_delete=models.CASCADE)
	acesso_c = models.ForeignKey(Acesso_r, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.conteudo)

