from django.urls import path
from .views import *

urlpatterns = [
    path('registrar/publicacao/<int:pub_id>/', request_denunciar_publicacao, name="request_denunciar_publicacao"),
    path('registrar/publicacao/',denunciar_publicacao, name="submeter_denuncia_publicacao" ),
    path('registrar/usuario/<int:usuario_id>/', request_denunciar_usuario, name="request_denunciar_usuario"),
    path('registrar/usuario/',denunciar_usuario, name="submeter_denuncia_usuario" ),
]
