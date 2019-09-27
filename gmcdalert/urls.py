from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^alerta$', views.alerta, name='alerta'),
	url(r'^delete_despesas$', views.delete_despesas, name='delete_despesas'),
	url(r'^teste$', views.teste, name='teste'),
	url(r'^sendalert$', views.sendalert, name='sendalert'),
	url(r'^contact_upload_conta$', views.contact_upload_conta, name='contact_upload_conta'),
	url(r'^contact_upload_unidade$', views.contact_upload_unidade, name='contact_upload_unidade'),
	url(r'^contact_upload_ccusto$', views.contact_upload_ccusto, name='contact_upload_ccusto'),
	url(r'^contact_upload_meta$', views.contact_upload_meta, name='contact_upload_meta'),
	url(r'^contact_upload_despesa$', views.contact_upload_despesa, name='contact_upload_despesa'),
	url(r'^contact_upload_responsavel$', views.contact_upload_responsavel, name='contact_upload_responsavel'),
	url(r'^relatorio$', views.relatorio, name='relatorio'),
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
