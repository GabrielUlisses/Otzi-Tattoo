from rest_framework import serializers

from .models import *
from usuario.serializers import UserSerializer

class NotificacaoSerializer(serializers.ModelSerializer ):
    class Meta:
        model = Notificacao
        fields = ['id','data_criacao','tipo','titulo','conteudo','emissor']

class NotificacaoUsuarioSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    notificacao = NotificacaoSerializer(read_only=True)
    
    class Meta:
        model = NotificacaoUsuario
        fields = ['id','usuario','notificacao','lido']