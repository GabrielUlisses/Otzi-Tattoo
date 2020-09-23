from django.contrib import admin
from .models import *

admin.site.register(Notificacao)
admin.site.register(TipoNotificacao)

@admin.register(NotificacaoUsuario)
class NotificacaoUsuarioAdmin(admin.ModelAdmin):
    class Meta:
        exclude = [ 'recebido']
