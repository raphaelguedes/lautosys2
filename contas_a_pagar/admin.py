from django.contrib import admin

from .models import Tipoconta
from .models import Conta

class ContaAdmin(admin.ModelAdmin):
	list_display = ('id','remetente','tipo', 'data_emissao', 'data_vencimento', 'rateio', 'data_envio', 'data_submissao','submissor','data_fiscalizacao','fiscal','data_pagamento','pagador','status')
	search_fields = ['remetente__usuario__username', 'tipo', 'data_emissao', 'id', 'data_vencimento','rateio','data_envio', 'data_submissao','submissor','data_fiscalizacao','fiscal','data_pagamento','pagador','status']
	ordering = [ 'id']

	def remetente(self, instance):
		return instance.remetente.usuario.username
	def tipo(self, instance):
		return instance.tipo.tipo
	def submissor(self, instance):
		return instance.submissor.username
	def fiscal(self, instance):
		return instance.fiscal.username
	def pagador(self, instance):
		return instance.pagador.username

admin.site.register(Tipoconta)
admin.site.register(Conta,ContaAdmin)