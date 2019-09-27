from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^addconta_controller$', views.addconta_controller, name='addconta_controller'),
	url(r'^minhascontas$', views.minhascontas, name='minhascontas'),
	url(r'^contas$', views.contas, name='contas'),
	url(r'^processamento_conta_controller$', views.processamento_conta_controller, name='processamento_conta_controller'),
	url(r'^fiscalizacao_conta_controller$', views.fiscalizacao_conta_controller, name='fiscalizacao_conta_controller'),
	url(r'^pagamento_conta_controller$', views.pagamento_conta_controller, name='pagamento_conta_controller'),
	url(r'^cancelamento_conta_controller$', views.cancelamento_conta_controller, name='cancelamento_conta_controller'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

