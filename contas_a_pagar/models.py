from django.db import models
from django.utils import timezone

from django.conf import settings
from django.contrib.auth.models import User

from django.db import models
import datetime

from lauto.models import User2
from lauto.models import Setor

###################################################################################################################

class Tipoconta(models.Model):
	tipo = models.CharField(max_length=75)

	def __str__(self):
		return self.tipo

class Conta(models.Model):
	remetente = models.ForeignKey(User2, on_delete=models.CASCADE, related_name='remetente')
	setor = models.ForeignKey(Setor, on_delete=models.CASCADE,null=True, blank=True)
	tipo = models.ForeignKey(Tipoconta, on_delete=models.CASCADE)
	data_emissao = models.DateField(null=True, blank=True)
	data_vencimento = models.DateField()
	valor = models.DecimalField(max_digits=8, decimal_places=2)
	rateio = models.TextField()
	observacao = models.TextField(null=True, blank=True)
	document = models.FileField(upload_to='documents/contas/%Y/%m')
	data_envio = models.DateTimeField(default=timezone.now)
	data_submissao = models.DateTimeField(null=True, blank=True)
	submissor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissor',null=True, blank=True)
	data_fiscalizacao = models.DateTimeField(null=True, blank=True)
	fiscal = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fiscal',null=True, blank=True)
	data_pagamento = models.DateTimeField(null=True, blank=True)
	pagador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pagador',null=True, blank=True)
	status = models.BooleanField(default=True)
	motivo_cancelamento = models.TextField(null=True, blank=True)
	cancelador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cancelador',null=True, blank=True)

	def __str__(self):
		return self.remetente.usuario.username