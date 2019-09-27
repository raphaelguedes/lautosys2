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
from django.core.files.storage import FileSystemStorage

from .models import Categoria
from .models import Tema
from .models import Curso
from .models import Modulo
from .models import Arquivo
from lauto.models import User2

from .forms import DocumentForm
from django import forms


from django.http import HttpResponse




def index(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	informacao = User2.objects.get(usuario = request.user)
	lista = Categoria.objects.order_by('nome_categoria')
	return render(request, 'ead/index.html',{'lista': lista,'informacao': informacao})

def novocurso(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	informacao = User2.objects.get(usuario = request.user)
	if not (informacao.tipo_user.id == 3 or informacao.tipo_user.id == 2):
		return HttpResponse ("Bloqueado - Somente gestores")
	lista = Tema.objects.order_by('nome_tema')
	return render(request, 'ead/novocurso.html',{'lista': lista})

def novocurso_controller(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	titulocurso = request.POST['titulocurso']
	conteudo = request.POST['conteudo']
	selectema = request.POST['selectema']
	Curso(titulo = titulocurso, tema = Tema.objects.get(id=selectema),conteudo=conteudo).save()
	return render(request, 'ead/index.html')

def infocategoria(request, categoriaid):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    info = Categoria.objects.get(id = categoriaid)
    lista = Tema.objects.filter(categoria=categoriaid).order_by('nome_tema')
    lista2 = Curso.objects.filter(tema__categoria = categoriaid).order_by('titulo')
    return render(request, 'ead/infocategoria.html',{'lista': lista,'info': info,'lista2': lista2})

def infocurso(request, cursoid):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    info = Curso.objects.get(id = cursoid)
    lista = Modulo.objects.filter(curso=cursoid).order_by('titulo')
    form = DocumentForm()
    lista2 = Arquivo.objects.filter(curso=cursoid).order_by('description')
    return render(request, 'ead/infocurso.html',{'lista': lista,'info': info,'informacao': informacao,'form': form,'lista2': lista2})

def infomodulo(request, cursoid, moduloid):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    info = Modulo.objects.get(id = moduloid)
    lista = Modulo.objects.filter(curso=cursoid).order_by('titulo')
    lista2 = Arquivo.objects.filter(curso=cursoid).order_by('description')
    return render(request, 'ead/infomodulo.html',{'info': info,'lista': lista,'informacao': informacao,'lista2': lista2})

def editarcurso(request, cursoid):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    info = Curso.objects.get(id = cursoid)
    informacao = User2.objects.get(usuario = request.user)
    if not (info.responsavel == request.user or informacao.tipo_user.id == 2):
    	return HttpResponse ("Bloqueado - Somente responsavel")
    lista = Tema.objects.order_by('nome_tema')
    lista2 = Modulo.objects.filter(curso=cursoid).order_by('titulo')
    return render(request, 'ead/editarcurso.html',{'lista': lista,'info': info,'lista2': lista2})

def editarcapacurso_controller(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	idcurso = request.POST['idcurso']
	titulocurso = request.POST['titulocurso']
	conteudo = request.POST['conteudo']
	selectema = request.POST['selectema']
	Curso.objects.filter(id=idcurso).update(titulo = titulocurso, tema= Tema.objects.get(id=selectema), conteudo = conteudo)
	return redirect('infocurso', cursoid = idcurso)

def editarmodulo(request, moduloid):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    info = Modulo.objects.get(id = moduloid)
    informacao = User2.objects.get(usuario = request.user)
    if not (info.curso.responsavel == request.user or informacao.tipo_user.id == 2):
    	return HttpResponse ("Bloqueado - Somente responsavel")
    return render(request, 'ead/editarmodulo.html',{'info': info})

def editarmodulocurso_controller(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	idcurso = request.POST['idcurso']
	idmodulo = request.POST['idmodulo']
	titulomodulo = request.POST['titulomodulo']
	conteudo = request.POST['conteudo']
	Modulo.objects.filter(id=idmodulo).update(titulo = titulomodulo, conteudo = conteudo)
	return redirect('infomodulo', moduloid = idmodulo, cursoid = idcurso)

def novomodulo(request,cursoid):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	info = Curso.objects.get(id = cursoid)
	informacao = User2.objects.get(usuario = request.user)
	if not (info.responsavel == request.user or informacao.tipo_user.id == 2):
		return HttpResponse ("Bloqueado - Somente responsavel")
	return render(request, 'ead/novomodulo.html',{'info': info})

def novomodulo_controller(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	titulomodulo = request.POST['titulomodulo']
	conteudo = request.POST['conteudo']
	idcurso = request.POST['idcurso']
	Modulo(titulo = titulomodulo, curso = Curso.objects.get(id=idcurso),conteudo=conteudo).save()
	return redirect('infocurso', cursoid = idcurso)

def upload(request):
	if not request.user.is_authenticated:
		return render(request, 'lauto/entrar.html')
	idcurso = request.POST['idcurso']
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form2 = Arquivo(curso = Curso.objects.get(id=idcurso), document=request.FILES['document'], description = request.POST['description'])
			form2.save()
			return redirect('infocurso', cursoid = idcurso)
	return redirect('infocurso', cursoid = idcurso)