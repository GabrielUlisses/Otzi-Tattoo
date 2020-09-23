from rest_framework import serializers
from .models import Tatuador

class TatuadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tatuador
        exclude = ["agenda","bio","endereco"]

class TatuadorSimpleSerializer(serializers.ModelSerializer):


    class Meta:
        model = Tatuador
        fields = ["telefone", "wathsapp","facebook","site_pessoal","instagram","usuario"]