from django.contrib import admin
from .models import *

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    models = Usuario
    exclude = ['ativo']

admin.site.register(PedidoOrcamento)