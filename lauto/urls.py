from django.conf.urls import url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^reset-password/$', password_reset, name='reset_password'),
	url(r'^reset-password/done/$', password_reset_done, name='password_reset_done'),
	url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
	url(r'^reset-password/complete/$', password_reset_complete, name='password_reset_complete'),
	###
	url(r'^entrar$', views.entrar, name='entrar'),
	url(r'^logout_controller$', views.logout_controller, name='logout_controller'),
	url(r'^login_controller$', views.login_controller, name='login_controller'),
	###
	url(r'^novo_usuario$', views.novo_usuario, name='novo_usuario'),
	url(r'^novo_usuario_controller$', views.novo_usuario_controller, name='novo_usuario_controller'),
	###
	url(r'^$', views.index, name='index'),
	url(r'^usuario$', views.usuario, name='usuario'),
	url(r'^teste$', views.teste, name='teste'),
	url(r'^alterar_usuario$', views.alterar_usuario, name='alterar_usuario'),
	url(r'^alterar_usuario_controller$', views.alterar_usuario_controller, name='alterar_usuario_controller'),
	####
	url(r'^controladoria$', views.controladoria, name='controladoria'),
	url(r'^institucional$', views.institucional, name='institucional'),
	url(r'^gerencia$', views.gerencia, name='gerencia'),
	url(r'^RH$', views.RH, name='RH'),
	url(r'^financeiro$', views.financeiro, name='financeiro'),
	url(r'^operacao$', views.operacao, name='operacao'),
	url(r'^CIL$', views.CIL, name='CIL'),
	url(r'^suprimentos$', views.suprimentos, name='suprimentos'),
	url(r'^TI$', views.TI, name='TI'),
	###
	url(r'^contact_upload_colaboradores$', views.contact_upload_colaboradores, name='contact_upload_colaboradores'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
