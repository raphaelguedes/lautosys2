from django.contrib import admin

from .models import Categoria
from .models import Tema
from .models import Curso
from .models import Modulo
from .models import Arquivo


admin.site.register(Categoria)
admin.site.register(Tema)
admin.site.register(Curso)
admin.site.register(Modulo)
admin.site.register(Arquivo)
