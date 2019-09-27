from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
from datetime import datetime
import csv, io
import numpy as np
import datetime as dt
from .forms import DocumentForm
from django import forms
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponse

from .models import Tipoconta
from .models import Conta
from gmcdalert.models import Ccusto
from gmcdalert.models import Unidade
from lauto.models import User2
from lauto.models import Acesso


def index(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	informacao = User2.objects.get(usuario = request.user)
	if Acesso.objects.filter(usuario = request.user, modulo__id = 12).exists() or informacao.tipo_user.id == 2:
		lista = Tipoconta.objects.order_by('tipo')
		lista2 = Unidade.objects.exclude(id=31).order_by('unidade_nome')
		lista3 = Ccusto.objects.order_by('ccusto_nome')
		form = DocumentForm()
		return render(request, 'contas_a_pagar/index.html', {'lista': lista,'lista2': lista2,'lista3': lista3,'form': form})
	else:
		return HttpResponse ("Bloqueado")

def addconta_controller(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	selectipo = request.POST['selectipo']
	rateio = ''
	lista = request.POST.getlist('checks')
	for column in lista:
		rateio = rateio + column + " - " 
	dataemissao = request.POST['dataemissao']
	datavencimento = request.POST['datavencimento']
	valor = request.POST['valor']
	informacaoadc = request.POST['informacaoadc']
	usuario = User2.objects.get(usuario=request.user)
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form2 = Conta(remetente = usuario, setor = usuario.setor, tipo = Tipoconta.objects.get(id=selectipo), data_emissao = dataemissao, data_vencimento = datavencimento, valor = valor, rateio = rateio, observacao = informacaoadc, document=request.FILES['document'])
			form2.save()
			return redirect('minhascontas')
	return redirect('index')

def minhascontas(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	lista = Conta.objects.filter(remetente__usuario = request.user)
	return render(request, 'contas_a_pagar/minhascontas.html', {'lista': lista})

def contas(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	informacao = User2.objects.get(usuario = request.user)
	if Acesso.objects.filter(usuario = request.user, modulo__id = 13).exists() or informacao.tipo_user.id == 2:
		lista = Conta.objects.all()
		acesso13 = Acesso.objects.filter(usuario = request.user, modulo__id = 13)
		acesso14 = Acesso.objects.filter(usuario = request.user, modulo__id = 14)
		acesso15 = Acesso.objects.filter(usuario = request.user, modulo__id = 15)
		return render(request, 'contas_a_pagar/contas.html', {'lista': lista,'acesso13': acesso13,'acesso14': acesso14, 'acesso15': acesso15,'active_tab':'recebidos'})
	elif Acesso.objects.filter(usuario = request.user, modulo__id = 14).exists():
		lista = Conta.objects.all()
		acesso13 = Acesso.objects.filter(usuario = request.user, modulo__id = 13)
		acesso14 = Acesso.objects.filter(usuario = request.user, modulo__id = 14)
		acesso15 = Acesso.objects.filter(usuario = request.user, modulo__id = 15)
		return render(request, 'contas_a_pagar/contas.html', {'lista': lista,'acesso13': acesso13,'acesso14': acesso14, 'acesso15': acesso15,'active_tab':'processada'})
	elif Acesso.objects.filter(usuario = request.user, modulo__id = 15).exists():
		lista = Conta.objects.all()
		acesso13 = Acesso.objects.filter(usuario = request.user, modulo__id = 13)
		acesso14 = Acesso.objects.filter(usuario = request.user, modulo__id = 14)
		acesso15 = Acesso.objects.filter(usuario = request.user, modulo__id = 15)
		return render(request, 'contas_a_pagar/contas.html', {'lista': lista,'acesso13': acesso13,'acesso14': acesso14, 'acesso15': acesso15,'active_tab':'fiscalizada'})
	else:
		return HttpResponse ("Bloqueado")

def processamento_conta_controller(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	informacao = User2.objects.get(usuario = request.user)
	if Acesso.objects.filter(usuario = request.user, modulo__id = 13).exists() or informacao.tipo_user.id == 2:
		idconta = request.POST['idconta']
		Conta.objects.filter(id = idconta).update(data_submissao = datetime.now(), submissor = request.user)
		return redirect('contas')
	else:
		return HttpResponse ("Bloqueado")

def fiscalizacao_conta_controller(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	informacao = User2.objects.get(usuario = request.user)
	if Acesso.objects.filter(usuario = request.user, modulo__id = 14).exists() or informacao.tipo_user.id == 2:
		idconta = request.POST['idconta']
		Conta.objects.filter(id = idconta).update(data_fiscalizacao = datetime.now(), fiscal = request.user)
		return redirect('contas')
	else:
		return HttpResponse ("Bloqueado")

def pagamento_conta_controller(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	informacao = User2.objects.get(usuario = request.user)
	if Acesso.objects.filter(usuario = request.user, modulo__id = 15).exists() or informacao.tipo_user.id == 2:
		idconta = request.POST['idconta']
		Conta.objects.filter(id = idconta).update(data_pagamento = datetime.now(), pagador = request.user)
		return redirect('contas')
	else:
		return HttpResponse ("Bloqueado")

def cancelamento_conta_controller(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	informacao = User2.objects.get(usuario = request.user)
	if Acesso.objects.filter(usuario = request.user, modulo__id = 13 or 14 or 15).exists() or informacao.tipo_user.id == 2:
		idconta = request.POST['idconta']
		motivo = request.POST['motivo']
		Conta.objects.filter(id = idconta).update(status = False, motivo_cancelamento = motivo, cancelador = request.user)
		return redirect('contas')
	else:
		return HttpResponse ("Bloqueado")