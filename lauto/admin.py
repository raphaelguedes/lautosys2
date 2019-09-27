from django.contrib import admin

from .models import Tipouser
from .models import Cargo
from .models import Setor
from .models import User2
from .models import Modulo
from .models import Acesso
from .models import Classe
from .models import Tipoveiculo
from .models import Marca
from .models import Modelo
from .models import Veiculos

################


class User2Admin(admin.ModelAdmin):
	list_display = ('matricula', 'nome', 'usuario', 'tipo_user', 'setor', 'cargo')
	search_fields = ['matricula', 'nome', 'usuario','setor', 'cargo']
	ordering = ['matricula']

	def usuario(self, instance):
		return instance.usuario.username


admin.site.register(Tipouser)
admin.site.register(Cargo)
admin.site.register(Setor)
admin.site.register(User2,User2Admin)
admin.site.register(Modulo)
admin.site.register(Acesso)
admin.site.register(Classe)
admin.site.register(Tipoveiculo)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(Veiculos)