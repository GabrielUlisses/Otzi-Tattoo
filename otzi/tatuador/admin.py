from django.contrib import admin
from tatuador.models import *

# class BioInline(admin.TabularInline):
#     models = Bio
    
class CertificacaoInline(admin.TabularInline):
   model = Certificacao
   extra = 1

@admin.register(Tatuador)
class TatuadorAdmin(admin.ModelAdmin):
    model = Tatuador
    inlines = [
        CertificacaoInline
    ]
    list_filter = ['data_criacao']

admin.site.register(Bio)
admin.site.register(Certificacao)
    