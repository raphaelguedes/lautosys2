from django.contrib import admin

# Register your models here.

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

class AcaoAdmin(admin.ModelAdmin):
	list_display = ('objetivo','responsavel_first_name', 'responsavel_last_name', 'prazo', 'area')
	search_fields = ['objetivo', 'responsavel__first_name', 'responsavel__last_name']
	ordering = ['responsavel__first_name']

	def responsavel_first_name(self, instance):
		return instance.responsavel.first_name
	def responsavel_last_name(self, instance):
		return instance.responsavel.last_name

class Acesso_rAdmin(admin.ModelAdmin):
	list_display = ('participante_first_name', 'participante_last_name', 'reuniao', 'tipo_acesso','status')
	search_fields = ['reuniao', 'participante__first_name', 'participante__last_name']
	ordering = ['participante__first_name']

	def participante_first_name(self, instance):
		return instance.participante.first_name
	def participante_last_name(self, instance):
		return instance.participante.last_name


admin.site.register(Reuniao)
admin.site.register(Acesso_r,Acesso_rAdmin)
admin.site.register(Area)
admin.site.register(Indicador)
admin.site.register(Status)
admin.site.register(Acao,AcaoAdmin)
admin.site.register(Tipo_r)
admin.site.register(Status_r)
admin.site.register(Tipo_acesso)
admin.site.register(Comentario2)
admin.site.register(Planoacao)