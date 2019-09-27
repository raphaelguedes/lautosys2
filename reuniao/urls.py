from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^teste$', views.teste, name='teste'),
	url(r'^reuniao_encerrada$', views.reuniao_encerrada, name='reuniao_encerrada'),
	url(r'^acao$', views.acao, name='acao'),
	url(r'^nova_reuniao$', views.nova_reuniao, name='nova_reuniao'),
	url(r'^nova_reuniao_controller$', views.nova_reuniao_controller, name='nova_reuniao_controller'),
	url(r'^reuniao/(?P<acesso_r__reuniao_id>[0-9]+)/$', views.inforeuniao, name='inforeuniao'),
	url(r'^acao/(?P<acao__acao_id>[0-9]+)/$', views.infoacao, name='infoacao'),
	url(r'^add_participante_controller$', views.add_participante_controller, name='add_participante_controller'),
	url(r'^editar_participante_controller$', views.editar_participante_controller, name='editar_participante_controller'),
	url(r'^remover_participante_controller$', views.remover_participante_controller, name='remover_participante_controller'),
	url(r'^nova_acao_controller$', views.nova_acao_controller, name='nova_acao_controller'),
	url(r'^atualizar_acao_controller$', views.atualizar_acao_controller, name='atualizar_acao_controller'),
	url(r'^atualizar_acao_controller2$', views.atualizar_acao_controller2, name='atualizar_acao_controller2'),
	url(r'^atualizar_reuniao_controller$', views.atualizar_reuniao_controller, name='atualizar_reuniao_controller'),
	url(r'^some_view$', views.some_view, name='some_view'),
	url(r'^faq_reuniao$', views.faq_reuniao, name='faq_reuniao'),
	url(r'^novo_comentario_controller$', views.novo_comentario_controller, name='novo_comentario_controller'),
	url(r'^atualizar_data_start_acao_controller$', views.atualizar_data_start_acao_controller, name='atualizar_data_start_acao_controller'),
	url(r'^adicionar_planoacao_controller$', views.adicionar_planoacao_controller, name='adicionar_planoacao_controller'),
	url(r'^atualizar_data_conclusao_acao_controller$', views.atualizar_data_conclusao_acao_controller, name='atualizar_data_conclusao_acao_controller'),
	url(r'^limpar_datas$', views.limpar_datas, name='limpar_datas'),
	url(r'^paginadiego$', views.paginadiego, name='paginadiego'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
