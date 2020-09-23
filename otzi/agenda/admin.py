from django.contrib import admin

from .models import *

class ConfiguracaoAgendaAdmin(admin.TabularInline):
    model = ConfiguracaoAgenda
    extra = 0
    min_num = 0
    max_num = 9

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin): 
    model = Agenda
    inlines = [
        ConfiguracaoAgendaAdmin
    ]

admin.site.register(ConfiguracaoAgenda)
'''
admin.site.register(ConclusaoTatuador)
admin.site.register(ConclusaoCliente)
'''