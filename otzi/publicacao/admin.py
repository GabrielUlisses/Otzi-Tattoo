from django.contrib import admin

from .models import *

admin.site.register(Aprovacao)

@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    fields = [('publicante','titulo'),'conteudo','midia']