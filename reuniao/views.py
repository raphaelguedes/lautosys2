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
import csv
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse

from .models import User
from .models import Reuniao
from .models import Acesso_r
from .models import Area
from .models import Indicador
from .models import Status
from .models import Acao
from .models import Tipo_r
from .models import Status_r
from .models import Tipo_acesso
from .models import Comentario2
from .models import Planoacao
from lauto.models import User2


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    lista = Acesso_r.objects.filter(participante = request.user,reuniao__status_r=1, status= True).order_by('reuniao__tipo_reuniao','reuniao__data')
    return render(request, 'reuniao/reuniao.html', {'lista': lista})

def acao(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao2 = Acao.objects.filter(responsavel = request.user).order_by('prazo')
    informacao3 = Acao.objects.filter(responsavel=request.user).order_by('objetivo')
    listcoment = Comentario2.objects.filter(acao_c__responsavel = request.user).values_list('acao_c',flat=True)
    now = timezone.now
    return render(request, 'reuniao/acao.html', {'listcoment': listcoment,'informacao2': informacao2,'informacao3':informacao3, 'now':now})

def nova_reuniao(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = User2.objects.get(usuario = request.user)
    if not (informacao.tipo_user.id == 3 or informacao.tipo_user.id == 2):
        return HttpResponse ("Bloqueado")
    lista = Tipo_r.objects.order_by('id')
    return render(request, 'reuniao/nova_reuniao.html',{'lista': lista})

def nova_reuniao_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'reuniao/entrar.html')

 
    pauta = request.POST['pauta']
    tituloreuniao = request.POST['tituloreuniao']
    descricaoreuniao = request.POST['descricaoreuniao']
    datareuniao = request.POST['datareuniao']
    timereuniao = request.POST['timereuniao']
    selecttipo_r = request.POST['selecttipo_r']
    datetime = datareuniao + " " + timereuniao
    Reuniao(titulo=tituloreuniao,assunto=descricaoreuniao, data=datetime, pauta = pauta,tipo_reuniao=Tipo_r.objects.get(id=selecttipo_r),status_r=Status_r.objects.get(id=1)).save()
    Acesso_r(participante = request.user,reuniao = Reuniao.objects.get(titulo=tituloreuniao,assunto=descricaoreuniao,pauta=pauta,data=datetime),tipo_acesso = Tipo_acesso.objects.get(id=2)).save()
    return redirect('/reuniao')

def inforeuniao(request, acesso_r__reuniao_id):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    if Acesso_r.objects.filter(reuniao = acesso_r__reuniao_id,participante=request.user,status = True).exists():
        tipoacesso = Acesso_r.objects.filter(reuniao = acesso_r__reuniao_id,participante=request.user)

        lista = Acesso_r.objects.filter(reuniao = acesso_r__reuniao_id, tipo_acesso__id = 1, status= True).order_by("participante__first_name")
        lista7 = Acesso_r.objects.filter(reuniao = acesso_r__reuniao_id, tipo_acesso__id = 2, status= True).order_by("participante__first_name")
        lista8 = Acesso_r.objects.filter(reuniao = acesso_r__reuniao_id, tipo_acesso__id = 3, status= True).order_by("participante__first_name")

        lista2 = User.objects.order_by('first_name') #[:5]
        lista3 = Area.objects.order_by('nome_area')
        lista4 = Indicador.objects.order_by('indicador')
        lista5 = Tipo_r.objects.order_by('tipo')
        lista6 = Status_r.objects.order_by('status_r')
        lista9 = Tipo_acesso.objects.order_by('id')
        informacao = get_object_or_404(Reuniao, pk=acesso_r__reuniao_id)
        informacao5 = Planoacao.objects.filter(reuniao=acesso_r__reuniao_id).order_by('nome')
        informacao2 = Acao.objects.filter(reuniao=acesso_r__reuniao_id).order_by('prazo')
        informacao3 = Acao.objects.filter(reuniao=acesso_r__reuniao_id,responsavel=request.user).order_by('objetivo')
        now = timezone.now
        listcoment = Comentario2.objects.filter(acao_c__reuniao__id = acesso_r__reuniao_id).values_list('acao_c',flat=True)
        listcoment2 = list(listcoment)
        return render(request, 'reuniao/inforeuniao.html', {'listcoment':listcoment,'listcoment2':listcoment2,'informacao': informacao, 'informacao5': informacao5, 'lista' : lista, 'lista2' : lista2,'lista3' : lista3,'lista4' : lista4,'lista5':lista5,'lista6':lista6,'lista7':lista7,'lista8':lista8,'tipoacesso':tipoacesso,'lista9':lista9,'now':now,'informacao2': informacao2,'informacao3': informacao3})   
    else:
        return HttpResponse ("Acesso negado")

def add_participante_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    reuniaoid = request.POST['reuniaoid']

    selectparticipante = request.POST['selectparticipante']
    selecttipo = request.POST['selecttipo']
    contador1 = Acesso_r.objects.filter(participante = User.objects.get(id=selectparticipante),reuniao = Reuniao.objects.get(id=reuniaoid)).count()
    if contador1==0:
        Acesso_r(participante = User.objects.get(id=selectparticipante),reuniao = Reuniao.objects.get(id=reuniaoid),tipo_acesso = Tipo_acesso.objects.get(id=selecttipo)).save()
    else:
        return HttpResponse ("Participante já tem ou teve acesso à reunião, solicite suporte ao TI.")
    reuniao_id = Reuniao.objects.get(id = reuniaoid).id
    return redirect('inforeuniao', acesso_r__reuniao_id = reuniao_id)

def editar_participante_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    reuniaoid = request.POST['reuniaoid']
    selectparticipante = request.POST['selectparticipante']
    selecttipo = request.POST['selecttipo']
    Acesso_r.objects.filter(participante = User.objects.get(id=selectparticipante),reuniao = Reuniao.objects.get(id=reuniaoid)).update(tipo_acesso = Tipo_acesso.objects.get(id=selecttipo))
    reuniao_id = Reuniao.objects.get(id = reuniaoid).id
    return redirect('inforeuniao', acesso_r__reuniao_id = reuniao_id)

def remover_participante_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    reuniaoid = request.POST['reuniaoid']
    selectparticipante = request.POST['selectparticipante']
    Acesso_r.objects.filter(participante = User.objects.get(id=selectparticipante),reuniao = Reuniao.objects.get(id=reuniaoid)).update(status = False)
    reuniao_id = Reuniao.objects.get(id = reuniaoid).id
    return redirect('inforeuniao', acesso_r__reuniao_id = reuniao_id)

def nova_acao_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    reuniaoid = request.POST['reuniaoid']
    selectresponsavel = request.POST['selectresponsavel']
    objetivoacao = request.POST['objetivoacao']
    motivoacao = request.POST['motivoacao']
    custoacao = request.POST['custoacao']
    atividadeacao = request.POST['atividadeacao']
    prazoacao = request.POST['prazoacao']
    timeprazo = request.POST['timeprazo']
    datetime = prazoacao + " " + timeprazo
    selectarea = request.POST['selectarea']
    selectplanoacao = request.POST['selectplanoacao']
    iniprevisto = request.POST['iniprevisto']
    timeiniprevisto = request.POST['timeiniprevisto']
    datetimeip = iniprevisto + " " + timeiniprevisto

    Acao(responsavel = User.objects.get(id=selectresponsavel),reuniao = Reuniao.objects.get(id=reuniaoid), data_inicioprevisto = datetimeip, prazo=datetime, objetivo = objetivoacao, motivo = motivoacao, custo = custoacao, atividade = atividadeacao, area = Area.objects.get(id=selectarea), planoacao = Planoacao.objects.get(id=selectplanoacao)).save()
    reuniao_id = Reuniao.objects.get(id=reuniaoid).id
    return redirect('inforeuniao', acesso_r__reuniao_id = reuniao_id)

def atualizar_acao_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    reuniaoid = request.POST['reuniaoid']

    selectacao = request.POST['selectacao']
    selecstatus = request.POST['selecstatus']
    if selecstatus == '1':
        Acao.objects.filter(id=selectacao).update(data_conclusao_acao = None, data_start_acao=None)
    elif selecstatus == '2':
        Acao.objects.filter(id=selectacao).update(data_start_acao= datetime.now())
    elif selecstatus == '3':
        Acao.objects.filter(id=selectacao).update(data_conclusao_acao = datetime.now())
    else:
        return HttpResponse ("Erro")
    if reuniaoid == "paginaacao":
    	return redirect('acao')
    else:
    	reuniao_id = Reuniao.objects.get(id=reuniaoid).id
    	return redirect('inforeuniao', acesso_r__reuniao_id = reuniao_id)

def atualizar_reuniao_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    reuniaoid = request.POST['reuniaoid']

    tituloreuniao = request.POST['tituloreuniao']
    assuntoreuniao = request.POST['assuntoreuniao']
    pautareuniao = request.POST['pautareuniao']
    datareuniao = request.POST['datareuniao']
    timereuniao = request.POST['timereuniao']
    selecttipo_r = request.POST['selecttipo_r']
    selectstatus_r = request.POST['selectstatus_r']
    datetime = datareuniao + " " + timereuniao

    Reuniao.objects.filter(id=reuniaoid).update(titulo=tituloreuniao,assunto=assuntoreuniao,data=datetime,pauta=pautareuniao,tipo_reuniao=Tipo_r.objects.get(id=selecttipo_r),status_r=Status_r.objects.get(id=selectstatus_r))
    reuniao_id = Reuniao.objects.get(id=reuniaoid).id
    return redirect('inforeuniao', acesso_r__reuniao_id = reuniao_id)

def infoacao(request, acao__acao_id):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    informacao = get_object_or_404(Acao, pk=acao__acao_id)
    lista2 = User.objects.order_by('first_name')
    lista3 = Area.objects.order_by('nome_area')
    lista4 = Indicador.objects.order_by('indicador')
    lista5 = Status.objects.order_by('id')
    lista6 = Acesso_r.objects.filter(reuniao = Reuniao.objects.get(id=informacao.reuniao.id), tipo_acesso__id = 2, status= True).order_by("participante__first_name")
    lista7 = Acesso_r.objects.filter(reuniao = Reuniao.objects.get(id=informacao.reuniao.id), tipo_acesso__id = 1, status= True).order_by("participante__first_name")
    lista8 = Comentario2.objects.filter(acao_c__id = acao__acao_id).order_by("data_c")
    tipoacesso = Acesso_r.objects.filter(reuniao = Reuniao.objects.get(id=informacao.reuniao.id),participante=request.user)
    informacao5 = Planoacao.objects.filter(reuniao=Reuniao.objects.get(id=informacao.reuniao.id)).order_by('id')
    now = timezone.now
    return render(request, 'reuniao/infoacao.html', {'informacao': informacao,'lista2': lista2,'lista3': lista3,'lista4': lista4,'lista5': lista5,'lista6': lista6,'lista7': lista7, 'lista8': lista8,'tipoacesso':tipoacesso,'now':now,'informacao5':informacao5})   

def atualizar_acao_controller2(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    reuniao_id =request.POST['reuniaoid']
    idacao=request.POST['idacao']
    objetivoacao = request.POST['objetivoacao']
    motivoacao = request.POST['motivoacao']
    selectresponsavel = request.POST['selectresponsavel']
    custoacao = request.POST['custoacao']
    atividadeacao = request.POST['atividadeacao']
    prazoacao = request.POST['prazoacao']
    timeprazo = request.POST['timeprazo']
    datetime = prazoacao + " " + timeprazo
    selectarea = request.POST['selectarea']
    selectpalnoacao = request.POST['selectpalnoacao']
    iniprevisto = request.POST['iniprevisto']
    timeiniprevisto = request.POST['timeiniprevisto']
    datetimeip = iniprevisto + " " + timeiniprevisto


    Acao.objects.filter(id=idacao).update(objetivo=objetivoacao,motivo=motivoacao,planoacao = Planoacao.objects.get(id = selectpalnoacao),responsavel=User.objects.get(id=selectresponsavel), custo = custoacao, atividade = atividadeacao,data_inicioprevisto = datetimeip, prazo=datetime,area=Area.objects.get(id=selectarea))
    return redirect('infoacao', acao__acao_id = idacao)

def atualizar_data_start_acao_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    reuniao_id =request.POST['reuniaoid']
    idacao=request.POST['idacao']
    inicioacao = request.POST['inicioacao']
    timeacao = request.POST['timeacao']
    datetime = inicioacao + " " + timeacao

    Acao.objects.filter(id=idacao).update(data_start_acao = datetime)
    return redirect('infoacao', acao__acao_id = idacao)

def atualizar_data_conclusao_acao_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    reuniao_id =request.POST['reuniaoid']
    idacao=request.POST['idacao']
    conclusaoacao = request.POST['conclusaoacao']
    timeacao = request.POST['timeacao']
    datetime = conclusaoacao + " " + timeacao

    Acao.objects.filter(id=idacao).update(data_conclusao_acao = datetime)
    return redirect('infoacao', acao__acao_id = idacao)

def limpar_datas(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    reuniao_id =request.POST['reuniaoid']
    idacao=request.POST['idacao']

    Acao.objects.filter(id=idacao).update(data_conclusao_acao = None, data_start_acao=None)
    return redirect('infoacao', acao__acao_id = idacao)

def reuniao_encerrada(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    lista = Acesso_r.objects.filter(participante = request.user,reuniao__status_r=2).order_by('reuniao__tipo_reuniao','reuniao__data')
    return render(request, 'reuniao/reuniao_encerrada.html', {'lista': lista})
    
def some_view(request):
    reuniaoid = request.POST['reuniaoid']
    lista = Acao.objects.filter(reuniao=Reuniao.objects.get(id=reuniaoid))
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Base de Dados Reunião.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([ 'Id','Plano de ação','Objetivo', 'Motivo', 'Responsável', 'Custo da ação', 'Atividades', 'Área', 'Data postado','Início previsto', 'Início', 'Conclusão', 'Prazo', 'Status'])
    for acao in lista:
        now = datetime.now(timezone.utc)
        if acao.data_i == None:
            datai = ' '   
        else:
            datai = acao.data_i.strftime("%d/%m/%Y")
        if acao.data_start_acao == None:
            datas = ' '
        else:
            datas = acao.data_start_acao.strftime("%d/%m/%Y")
        if acao.data_conclusao_acao == None:
            datac = ' '
        else:
            datac = acao.data_conclusao_acao.strftime("%d/%m/%Y")
        if acao.data_inicioprevisto == None:
            dataiprevisto = ' '   
        else:
            dataiprevisto = acao.data_inicioprevisto.strftime("%d/%m/%Y")
        if acao.prazo == None:
            datap = ' '
        else:
            datap = acao.prazo.strftime("%d/%m/%Y")       
        if  acao.data_conclusao_acao != None and acao.data_conclusao_acao > acao.prazo:
            status = 'Concluido com atraso'
        elif acao.data_conclusao_acao != None and acao.data_conclusao_acao <= acao.prazo:
            status = 'Concluido'
        elif acao.data_start_acao!= None and acao.data_start_acao >= acao.data_i and now > acao.prazo:
            status = 'Em andamento com atraso'
        elif acao.data_start_acao!= None and acao.data_start_acao >= acao.data_i:
            status = 'Em andamento'
        elif now > acao.prazo:
            status = 'Atrasado'
        else:
            status = 'Não iniciado'

        writer.writerow([
        acao.id,
        acao.planoacao.nome,
        acao.objetivo,
        acao.motivo,
        acao.responsavel.first_name + ' ' + acao.responsavel.last_name,
        acao.custo,
        acao.atividade,
        acao.area.nome_area,
        datai,
        dataiprevisto,
        datas,
        datac,
        datap,
        status
        ])

    return response

def teste(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    lista = Acao.objects.filter(responsavel = request.user).order_by('data_f')
    return render(request, 'reuniao/acao.html', {'lista': lista})

def faq_reuniao(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')
    return render(request, 'reuniao/faq_reuniao.html')

def novo_comentario_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    comentario2acao = request.POST['comentario2acao']
    idacao=request.POST['idacao']
    reuniao_id =request.POST['reuniaoid']
    Comentario2(conteudo=comentario2acao,acao_c=Acao.objects.get(id=idacao),acesso_c=Acesso_r.objects.get(participante=request.user,reuniao=reuniao_id)).save()

    return redirect('infoacao', acao__acao_id = idacao)

def adicionar_planoacao_controller(request):
    if not request.user.is_authenticated:
        return render(request, 'lauto/entrar.html')

    planoacao = request.POST['planoacao']
    reuniaoid = request.POST['reuniaoid']
    Planoacao(nome=planoacao,reuniao = Reuniao.objects.get(id=reuniaoid)).save()
    reuniao_id = Reuniao.objects.get(id=reuniaoid).id
    return redirect('inforeuniao', acesso_r__reuniao_id = reuniao_id)

def paginadiego(request):
    return render(request, 'reuniao/paginadiego.html')