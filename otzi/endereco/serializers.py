from rest_framework import serializers
from .models import Endereco

from tatuador.serializers import TatuadorSerializer
from tatuador.models import Tatuador



class EnderecoSerializer(serializers.ModelSerializer):
    tatuador = serializers.SerializerMethodField(method_name="get_tatuador")

    class Meta:    
        model = Endereco
        fields = ['id','estado','cidade','bairro','rua','numero','complemento','cep','tatuador']  

    def get_tatuador(self, studio):
        tatuador = TatuadorSerializer(Tatuador.objects.get(endereco=studio))
        return tatuador.data