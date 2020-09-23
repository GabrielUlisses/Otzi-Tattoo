from django.shortcuts import render, redirect

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import  APIView
from rest_framework.decorators import action

import json

from .models import Notificacao, TipoNotificacao, NotificacaoUsuario, User
from usuario.models import Usuario
from .serializers import NotificacaoUsuarioSerializer, NotificacaoSerializer

def gerar_notificacao(*destinatarios,**kwargs):
    n = Notificacao.objects.create(
        titulo = kwargs.get('titulo'),
        emissor = kwargs.get('emissor'),
        conteudo = kwargs.get('conteudo'),
        tipo = kwargs.get('tipo'),
    )   
    for i in destinatarios:
        n.destinatarios.add(i)
    n.save()  
    return n

def carregar_notificacoes(request):
    """
    View responsável por carregar todas as notificações do usuário, enviadas e recebidas.
    """
    template_name = 'notificacao/notificacoes.html'
    context = {
        'notificacoes': NotificacaoUsuario.objects.filter(usuario = request.user.id).order_by('-notificacao_id'),
    }
    return render(request, template_name, context)

def remover_notificacao(request, not_pk):
    notificacao = Notificacao.objects.get(id = not_pk)
    notificacao.delete()
    return redirect('notificacoes')
    

##### REST FRAMEWORK #####

class NotificacaoSetLidoApiView(APIView):  
    def get(self, request, user_pk, not_pk):
        obj = NotificacaoUsuario.objects.filter(usuario = user_pk, notificacao = not_pk)
        if len(obj) > 0:
            obj = obj[0]
            obj.lido = True
            obj.save()
        serializer = NotificacaoUsuarioSerializer(obj)
        return Response(serializer.data)

class NotificacaoUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacaoUsuarioSerializer
    queryset = NotificacaoUsuario.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = NotificacaoUsuario.objects.filter(usuario = request.user.id)
        serializer = NotificacaoUsuarioSerializer( queryset, many=True )
        return Response(serializer.data)

class NotificacaoViewSet(viewsets.ModelViewSet):
    queryset = Notificacao.objects.all()
    serializer_class = NotificacaoSerializer

def parse_json(data):
    return json.dumps(data)
