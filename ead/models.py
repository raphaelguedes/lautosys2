from django.db import models
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import User

from django.db import models
import datetime

class Categoria(models.Model):
	nome_categoria = models.CharField(max_length=50)
	def __str__(self):
		return str(self.nome_categoria)


class Tema(models.Model):
	nome_tema = models.CharField(max_length=100)
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.nome_tema)

class Curso(models.Model):
	titulo = models.CharField(max_length=200)
	tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
	conteudo = models.TextField()
	responsavel = models.ForeignKey(User, on_delete=models.CASCADE)
	data_criacao = models.DateTimeField(default=timezone.now)
	data_atualizacao = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return str(self.titulo)

class Modulo(models.Model):
	titulo = models.CharField(max_length=400)
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
	conteudo = models.TextField()

	def __str__(self):
		return str(self.titulo)

class Arquivo(models.Model):
	description = models.CharField(max_length=255, blank=True, null=True)
	document = models.FileField(upload_to='documents/ead')
	uploaded_at = models.DateTimeField(default=timezone.now)
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.description)