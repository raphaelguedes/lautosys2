from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^novocurso$', views.novocurso, name='novocurso'),
	url(r'^novocurso_controller$', views.novocurso_controller, name='novocurso_controller'),
	url(r'^categoria/(?P<categoriaid>[0-9]+)/$', views.infocategoria, name='infocategoria'),
	url(r'^curso/(?P<cursoid>[0-9]+)/$', views.infocurso, name='infocurso'),
	url(r'^curso/(?P<cursoid>[0-9]+)/modulo/(?P<moduloid>[0-9]+)$', views.infomodulo, name='infomodulo'),
	url(r'^editarcurso/(?P<cursoid>[0-9]+)$', views.editarcurso, name='editarcurso'),
	url(r'^editarcapacurso_controller$', views.editarcapacurso_controller, name='editarcapacurso_controller'),
	url(r'^editarmodulo/(?P<moduloid>[0-9]+)$', views.editarmodulo, name='editarmodulo'),
	url(r'^editarmodulocurso_controller$', views.editarmodulocurso_controller, name='editarmodulocurso_controller'),
	url(r'^adicionarmodulo/(?P<cursoid>[0-9]+)$', views.novomodulo, name='novomodulo'),
	url(r'^novomodulo_controller$', views.novomodulo_controller, name='novomodulo_controller'),
	url(r'^upload$', views.upload, name='upload'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

