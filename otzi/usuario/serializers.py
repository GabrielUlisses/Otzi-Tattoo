from rest_framework import serializers

from tatuador.serializers import TatuadorSerializer
from publicacao.serializers import PublicacaoSerializer

from .models import PedidoOrcamento, User, Usuario
from publicacao.models import Publicacao


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','email']

class UsuarioSerializer(serializers.ModelSerializer):
    tatuador = TatuadorSerializer(read_only=True)
    usuario = UserSerializer(read_only=True)
    publicacoes = serializers.SerializerMethodField(method_name="get_lasted_five_publications")

    class Meta:
        model = Usuario 
        fields = ['id','nome','tatuador','desenhista','imagem','usuario','publicacoes']

    def get_lasted_five_publications(self,user):
        publicacoes = PublicacaoSerializer(Publicacao.objects.filter(publicante=user.usuario)[:5], many=True)
        return publicacoes.data

class UsuarioSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario 
        fields = ['id','nome','email','tatuador']

class PedidoOrcamentoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    tatuadores = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = PedidoOrcamento
        fields = ['id','usuario','tatuadores','titulo','texto_receptivo','parte_corpo','img_1','img_2','img_3','texto_complementar','valor_esperado','tamanho']

class PedidoOrcamentoSimpleSerializer(serializers.ModelSerializer):
    usuario = serializers.HyperlinkedRelatedField(view_name="User-details",read_only=True)
    class Meta:
        model = PedidoOrcamento
        fields = ['id','usuario','tatuadores']
