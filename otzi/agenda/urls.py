from django.urls import path
from .views import *

urlpatterns = [
    path('configuracao/registro/', formulario_configuracao_agenda, name="registro_configuracao"),
    path('configuracao/formulario_de_edição/', request_editar_configuracao_agenda, name="request_editar_configuracao" ),
    path('configuracao/salvar_alterações/', editar_configuracao_agenda, name="editar_configuracao" ),
    path('configuracao/configurar/', configurar_configuracao_agenda, name="configurar_dia_agenda"),
    path('configuracao/configurar/request/', request_configurar_configuracao_agenda, name="request_configurar_dia_agenda"),
    path('configuracao/remove/', remover_configuracao_agenda, name="remover_configuracao_agenda"),
]
