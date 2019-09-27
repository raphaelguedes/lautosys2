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
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from django.db.models import Count
from itertools import chain
from django import db
from django.core.mail import send_mail
from django.utils.translation import gettext
from django.core import mail
from django.template.loader import render_to_string

from django.http import HttpResponse

from .models import Conta
from .models import Responsavel
from .models import Unidade
from .models import Ccusto
from .models import Meta
from .models import Despesa
from .models import Alerta
from .models import User
from lauto.models import User2
from lauto.models import Acesso

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if Acesso.objects.filter(usuario = request.user, modulo__id = 1).exists() or informacao.tipo_user.id == 2:
        lista = Ccusto.objects.order_by('unidade__unidade_nome')
        return render(request, 'gmcdalert/index.html',{'lista': lista})
    else:
        return HttpResponse ("Bloqueado")

def alerta(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if Acesso.objects.filter(usuario = request.user, modulo__id = 1).exists() or informacao.tipo_user.id == 2:
        mes = request.POST['selectmes']
        lista = Despesa.objects.filter(data__month=mes).values('conta__conta_nome','ccusto__ccusto_nome', 'ccusto__responsavel__nome','ccusto__gerente__first_name','chave_meta__valor_meta', 'chave_meta__chave_meta').order_by('conta__conta_nome').annotate(sum_despesa=Sum('valor_despesa'))
        listaalertas = list(Alerta.objects.values_list('chave_meta__chave_meta',flat=True).all())
        quantidade = Alerta.objects.filter(chave_meta__data__month=mes).count()
        grafico = Alerta.objects.filter(chave_meta__data__month=mes).values('chave_meta__ccusto__responsavel__nome').annotate(count_alerta=Count('chave_meta__ccusto__responsavel__nome')).order_by('-count_alerta')
        grafico2 = Alerta.objects.filter(chave_meta__data__month=mes).values('chave_meta__ccusto__ccusto_nome').annotate(count_alerta=Count('chave_meta__ccusto__ccusto_nome')).order_by('-count_alerta')
    
#    grafico = Alerta.objects.filter(chave_meta__data__month=mes,chave_meta__ccusto__regional = 37  ).values('chave_meta__ccusto__responsavel__nome').annotate(count_alerta=Count('chave_meta__ccusto__responsavel__nome')).order_by('-count_alerta')
#	lista2 = Meta.objects.filter(data__month=mes).values_list('conta__conta_nome',flat=True)
#	lista2 = Meta.objects.filter(data__month=mes).values('conta__conta_nome','ccusto__ccusto_nome').order_by('conta__conta_nome').annotate(sum_meta=Sum('valor_meta'))
#	listaalerta = lista | lista2
#list()
        return render(request, 'gmcdalert/alerta.html',{'lista': lista,'listaalertas': listaalertas,'quantidade': quantidade,'grafico': grafico,'grafico2': grafico2})
    else:
        return HttpResponse ("Bloqueado")


def contact_upload_conta(request):
    template = "gmcdalert/contact_upload_conta.html"

    prompt = {
        'order': "Order of csv should be id, nome da conta"
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This file is not a .csv file")

    data_set = csv_file.read().decode('utf-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Conta.objects.update_or_create(
            conta_nome=column[0]
        )

    context = {}
    return render(request, template, context)

def contact_upload_unidade(request):
    template = "gmcdalert/contact_upload_unidade.html"

    prompt = {
        'order': "Order of csv should be nome da unidade"
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This file is not a .csv file")

    data_set = csv_file.read().decode('utf-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Unidade.objects.update_or_create(
            unidade_nome=column[0]
        )

    context = {}
    return render(request, template, context)

def contact_upload_responsavel(request):
    template = "gmcdalert/contact_upload_responsavel.html"

    prompt = {
        'order': "Order of csv should be nome, e-mail"
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This file is not a .csv file")

    data_set = csv_file.read().decode('utf-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=';', quotechar="|"):
        _, created = Responsavel.objects.update_or_create(
            nome = column[0],
            defaults={
            'email': column[1]}
        )

    context = {}
    return render(request, template, context)

def contact_upload_ccusto(request):
    template = "gmcdalert/contact_upload_ccusto.html"

    prompt = {
        'order': "Order of csv should be nome do centro de custo, unidade, responsável"
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This file is not a .csv file")

    data_set = csv_file.read().decode('utf-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=';', quotechar="|"):
        _, created = Ccusto.objects.update_or_create(
        	ccusto_nome = column[2],
#        	unidade = Unidade.objects.get(unidade_nome=column[1])
        	            defaults={
            'responsavel': Responsavel.objects.get(nome=column[0])}
        )
        

    context = {}
    return render(request, template, context)

def contact_upload_meta(request):
    template = "gmcdalert/contact_upload_meta.html"

    prompt = {
        'order': "Order of csv should be nome conta, centro de custo, data e valor"
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This file is not a .csv file")

    data_set = csv_file.read().decode('utf-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=';', quotechar="|"):

        _, created = Meta.objects.update_or_create(
            chave_meta = column[3],
            defaults={'conta': Conta.objects.get(conta_nome=column[0]),
            'ccusto':Ccusto.objects.get(ccusto_nome=column[1]),
            'data' : datetime.strptime(column[2], '%d/%m/%Y').strftime("%Y-%m-%d"),
            'valor_meta': column[4].replace(",", ".")}
        )

    context = {}
    return render(request, template, context)

def contact_upload_despesa(request):
    template = "gmcdalert/contact_upload_despesa.html"

    prompt = {
        'order': "A ordem do CSV deve ser: nome da conta, centro de custo, data, valor, chave da despesa e chave da meta"
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "This file is not a .csv file")

    data_set = csv_file.read().decode('utf-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=';', quotechar="|"):
    	try:
	        _, created = Despesa.objects.update_or_create(
            chave_despesa = column[4],
            defaults={'conta': Conta.objects.get(conta_nome=column[0]),
            'ccusto':Ccusto.objects.get(ccusto_nome=column[1]),
            'data' : datetime.strptime(column[2], '%d/%m/%Y').strftime("%Y-%m-%d"),
            'valor_despesa': column[3].replace(",", "."),
            'chave_meta': Meta.objects.get(chave_meta=column[5])}
        )

    	except Meta.DoesNotExist:
	        _, created = Despesa.objects.update_or_create(
            chave_despesa = column[4],
            defaults={'conta': Conta.objects.get(conta_nome=column[0]),
            'ccusto':Ccusto.objects.get(ccusto_nome=column[1]),
            'data' : datetime.strptime(column[2], '%d/%m/%Y').strftime("%Y-%m-%d"),
            'valor_despesa': column[3].replace(",", "."),
            'chave_meta': Meta.objects.get(chave_meta='zero')}
        )

    context = {}
    return render(request, template, context)


def delete_despesas(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	Meta.objects.all().delete()
	return render(request, 'gmcdalert/index.html')

def teste(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	return render(request, 'gmcdalert/teste.html')

def sendalert(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    lista = request.POST.getlist('checks')
    connection = mail.get_connection()   
    for column in lista:
        info = Meta.objects.get(chave_meta = column)
        email = info.ccusto.responsavel.email
        conta = info.conta
        valor = info.valor_meta
        ccusto = info.ccusto.ccusto_nome
        unidade = info.ccusto.unidade.unidade_nome
        responsavel = info.ccusto.responsavel.nome
        mes = gettext(info.data.strftime('%B'))
        titulo = render_to_string('gmcdalert/emailtitulo.html', {'conta': conta})
        mensagem = render_to_string('gmcdalert/emailmensagem.html', {'email': email,'conta': conta,'valor': valor,'ccusto': ccusto,'unidade': unidade,'responsavel': responsavel,'mes': mes})
        sendemail = mail.EmailMessage(
#        send_mail(
    titulo,
    mensagem,
    'intralautosystem@gmail.com',
    [email]
)
        sendemail.send()
        Alerta(chave_meta = Meta.objects.get(chave_meta = column)).save()
    connection.close()

    return redirect('/lauto/controladoria')

def relatorio(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    mes = request.POST['selectmes']
    lista = Despesa.objects.filter(data__month=mes,ccusto__gerente = request.user).values('conta__conta_nome','ccusto__ccusto_nome', 'ccusto__responsavel__nome','ccusto__gerente__first_name','chave_meta__valor_meta', 'chave_meta__chave_meta').order_by('conta__conta_nome').annotate(sum_despesa=Sum('valor_despesa'))
    listaalertas = list(Alerta.objects.values_list('chave_meta__chave_meta',flat=True).all())
    quantidade = Alerta.objects.filter(chave_meta__data__month=mes,chave_meta__ccusto__gerente=request.user).count()
    grafico = Alerta.objects.filter(chave_meta__data__month=mes,chave_meta__ccusto__gerente=request.user).values('chave_meta__ccusto__responsavel__nome').annotate(count_alerta=Count('chave_meta__ccusto__responsavel__nome')).order_by('-count_alerta')
    grafico2 = Alerta.objects.filter(chave_meta__data__month=mes,chave_meta__ccusto__gerente=request.user).values('chave_meta__ccusto__ccusto_nome').annotate(count_alerta=Count('chave_meta__ccusto__ccusto_nome')).order_by('-count_alerta')
    return render(request, 'gmcdalert/relatorio.html',{'lista': lista,'listaalertas': listaalertas,'quantidade': quantidade,'grafico': grafico,'grafico2': grafico2})