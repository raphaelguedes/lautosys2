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

from django.http import HttpResponse


from .models import User2
from .models import User
from .models import Tipouser
from gmcdalert.models import Ccusto
from .models import Modulo
from .models import Acesso
from .models import Setor

def entrar(request):
	return render(request, 'lauto/entrar.html',)

def login_controller(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        contador = User2.objects.filter(usuario = request.user, status=True).count() 
        if contador == 0:
        	return redirect('alterar_usuario')
        else:
            return redirect('index')
    else:
        return HttpResponse ("Login invalido")

def alterar_usuario(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.filter(usuario = request.user)
    return render(request, 'lauto/alterar_usuario.html',{'informacao': informacao})

def alterar_usuario_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    nome = request.POST['nome']
    sobrenome = request.POST['sobrenome']
    cpf = request.POST['cpf']
    telefone1 = request.POST['telefone1']
    telefone2 = request.POST['telefone2']
    datan = request.POST['datan']
    contador = User2.objects.filter(usuario = request.user).count() 
    if contador == 0:
        User.objects.filter(username=request.user).update(first_name = nome, last_name = sobrenome)
        User2(usuario = User.objects.get(username=request.user), cpf = cpf, telefone_1 =telefone1, telefone_2= telefone2, datan=datan, status = True, tipo_user= Tipouser.objects.get(id=1)).save()
        return redirect('index')
    else:
        User.objects.filter(username=request.user).update(first_name = nome, last_name = sobrenome)
        User2.objects.filter(usuario = request.user).update(cpf = cpf, telefone_1 =telefone1,telefone_2= telefone2, datan=datan, status = True,tipo_user= Tipouser.objects.get(id=1))
        return redirect('usuario')

def logout_controller(request):
    logout(request)
    return redirect('entrar')

def index(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	return render(request, 'lauto/index.html')

def novo_usuario(request):
    return render(request,'lauto/novo_usuario.html',)

def novo_usuario_controller(request):
    username = request.POST['username']
    email = request.POST['email']
    psw = request.POST['psw']
    pswrepeat = request.POST['pswrepeat']
    if psw==pswrepeat:
        contador1 = User.objects.filter(email= email).count()
        contador2 = User.objects.filter(username= username).count()
        if contador1==0 and contador2==0:
            User.objects.create_user(username= username,email = email,password = psw)
            return redirect('entrar')
        else:
            return redirect('erro')
    else:
        return redirect('erro')


def usuario(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.filter(usuario = request.user)
    return render(request, 'lauto/usuario.html', {'informacao': informacao})

def teste(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    lista = Acao.objects.filter(responsavel = request.user).order_by('data_f')
    return render(request, 'lauto/acao.html', {'lista': lista})

def controladoria(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if Acesso.objects.filter(usuario = request.user, modulo__id = 1).exists() or informacao.tipo_user.id == 2:
        return render(request, 'lauto/controladoria.html')
    else:
        return HttpResponse ("Bloqueado")

def institucional(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    return render(request, 'lauto/institucional.html')

def gerencia(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if not (informacao.tipo_user.id == 3 or informacao.tipo_user.id == 2):
        return HttpResponse ("Bloqueado")
    lista = Ccusto.objects.filter(gerente = request.user).order_by('ccusto_nome')
    return render(request, 'lauto/gerencia.html', {'lista': lista})

def contact_upload_colaboradores(request):
    template = "lauto/contact_upload_colaboradores.html"

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

        _, created = User2.objects.update_or_create(
            matricula = column[0],
            defaults={'nome': column[1],
            'cpf': column[2],
            'datan' : datetime.strptime(column[8], '%d/%m/%Y').strftime("%Y-%m-%d"),
            'setor': Setor.objects.get(nome_setor=column[13])
            }
        )

    context = {}
    return render(request, template, context)

def RH(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if Acesso.objects.filter(usuario = request.user, modulo__id = 2).exists() or informacao.tipo_user.id == 2:
    	start = dt.date( 2019, 7, 10 )
    	end = dt.date( 2019, 7, 22 )
    	days = np.busday_count( start, end )
    	return render(request, 'lauto/RH.html', {'days': days})
    else:
        return HttpResponse ("Bloqueado")

def financeiro(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if Acesso.objects.filter(usuario = request.user, modulo__id = 3).exists() or informacao.tipo_user.id == 2:
        return render(request, 'lauto/financeiro.html')
    else:
        return HttpResponse ("Bloqueado")

def operacao(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if Acesso.objects.filter(usuario = request.user, modulo__id = 4).exists() or informacao.tipo_user.id == 2:
        return render(request, 'lauto/operacao.html')
    else:
        return HttpResponse ("Bloqueado")

def CIL(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if Acesso.objects.filter(usuario = request.user, modulo__id = 5).exists() or informacao.tipo_user.id == 2:
        return render(request, 'lauto/CIL.html')
    else:
        return HttpResponse ("Bloqueado")

def suprimentos(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if Acesso.objects.filter(usuario = request.user, modulo__id = 6).exists() or informacao.tipo_user.id == 2:
        return render(request, 'lauto/suprimentos.html')
    else:
        return HttpResponse ("Bloqueado")

def TI(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if Acesso.objects.filter(usuario = request.user, modulo__id = 7).exists() or informacao.tipo_user.id == 2:
        return render(request, 'lauto/TI.html')
    else:
        return HttpResponse ("Bloqueado")

def contact_upload_veiculos(request):
    template = "lauto/contact_upload_veiculos.html"

    prompt = {
        'order': "Order of csv should be "
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

        _, created = User2.objects.update_or_create(
            placa = column[0],
            defaults={'nome': column[1],
            'cpf': column[2],
            'datan' : datetime.strptime(column[8], '%d/%m/%Y').strftime("%Y-%m-%d"),
            'setor': Setor.objects.get(nome_setor=column[13])
            }
        )

    context = {}
    return render(request, template, context)