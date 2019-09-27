from django.contrib import admin

from .models import Conta
from .models import Responsavel
from .models import Unidade
from .models import Ccusto
from .models import Meta
from .models import Despesa
from .models import Alerta

class MetaAdmin(admin.ModelAdmin):
	list_display = ('id','conta_conta_nome','ccusto_ccusto_nome', 'ccusto_unidade_unidade_nome', 'data', 'valor_meta', 'chave_meta')
	search_fields = ['conta__conta_nome', 'ccusto__ccusto_nome', 'data', 'id', 'chave_meta']
	ordering = [ 'id','conta__conta_nome']

	def conta_conta_nome(self, instance):
		return instance.conta.conta_nome
	def ccusto_ccusto_nome(self, instance):
		return instance.ccusto.ccusto_nome
	def ccusto_unidade_unidade_nome(self, instance):
		return instance.ccusto.unidade.unidade_nome

class DespesaAdmin(admin.ModelAdmin):
	list_display = ('id','conta_conta_nome','ccusto_ccusto_nome', 'ccusto_unidade_unidade_nome', 'data', 'valor_despesa', 'chave_meta_chave_meta')
	search_fields = ['conta__conta_nome', 'ccusto__ccusto_nome', 'data', 'id']
	ordering = [ 'id','conta__conta_nome']

	def conta_conta_nome(self, instance):
		return instance.conta.conta_nome
	def ccusto_ccusto_nome(self, instance):
		return instance.ccusto.ccusto_nome
	def ccusto_unidade_unidade_nome(self, instance):
		return instance.ccusto.unidade.unidade_nome
	def chave_meta_chave_meta(self, instance):
		return instance.chave_meta.chave_meta

class CcustoAdmin(admin.ModelAdmin):
	list_display = ('id','ccusto_nome','unidade_unidade_nome', 'responsavel_nome', 'responsavel_email', 'gerente_first_name')
	search_fields = ['ccusto_nome', 'unidade__unidade_nome', 'responsavel__nome', 'responsavel__email', 'gerente__first_name']
	ordering = [ 'id','ccusto_nome']

	def unidade_unidade_nome(self, instance):
		return instance.unidade.unidade_nome
	def responsavel_nome(self, instance):
		return instance.responsavel.nome
	def responsavel_email(self, instance):
		return instance.responsavel.email
	def gerente_first_name(self, instance):
		return instance.gerente.first_name

class AlertaAdmin(admin.ModelAdmin):
	list_display = ('id','chave_meta_conta_conta_nome','chave_meta_ccusto_ccusto_nome', 'chave_meta_ccusto_responsavel_nome', 'chave_meta_ccusto_gerente_first_name', 'chave_meta_data', 'data')
	search_fields = ['chave_meta__conta__conta_nome', 'chave_meta__ccusto__ccusto_nome', 'chave_meta__ccusto__responsavel__nome', 'chave_meta__ccusto__gerente__first_name', 'chave_meta__data', 'data']
	ordering = [ 'id']

	def chave_meta_conta_conta_nome(self, instance):
		return instance.chave_meta.conta.conta_nome
	def chave_meta_ccusto_ccusto_nome(self, instance):
		return instance.chave_meta.ccusto.ccusto_nome
	def chave_meta_ccusto_responsavel_nome(self, instance):
		return instance.chave_meta.ccusto.responsavel.nome
	def chave_meta_ccusto_gerente_first_name(self, instance):
		return instance.chave_meta.ccusto.gerente.first_name
	def chave_meta_data(self, instance):
		return instance.chave_meta.data


admin.site.register(Conta)
admin.site.register(Responsavel)
admin.site.register(Unidade)
admin.site.register(Ccusto,CcustoAdmin)
admin.site.register(Meta,MetaAdmin)
admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Alerta,AlertaAdmin)