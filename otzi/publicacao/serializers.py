from rest_framework import serializers

from .models import Publicacao, Aprovacao

class PublicacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacao
        fields = ["titulo","conteudo","publicante","midia","nr_aprovacoes"]

class AprovacaoSerializer(serializers.ModelSerializer):
    publicacao = PublicacaoSerializer()

    class Meta:
        model = Aprovacao
        fields = ['publicacao','usuario']