from django.shortcuts import render, get_object_or_404
from publicacao.models import Publicacao, Aprovacao
from usuario.models import Usuario

import datetime

def index(request):
    """
    Além de desempenhar o papel de página principal do sistema, esta view é responsável por listar as 100 últimas publica-
    ções realizadas no dia, ordenando-as pelo número de aprovações de modo decrescente
    """
    template_name = 'index.html'
    hoje = datetime.datetime.now()
    if request.user.is_authenticated:
        aprovacoes = Aprovacao.objects.filter(usuario=get_object_or_404(Usuario, usuario=request.user))
        context = { 'publicacoes': [ { 'publicacao':publicacao, 'aprovacao':aprovacoes.filter(publicacao=publicacao).first() }  for publicacao in Publicacao.objects.filter(data_criacao__gt=datetime.date(hoje.year, hoje.month, hoje.day)).order_by('-nr_aprovacoes')][0:100] }
    else:
        context = { 'publicacoes': [ { 'publicacao':publicacao, 'aprovacao':None }  for publicacao in Publicacao.objects.filter(data_criacao__gt=datetime.date(hoje.year, hoje.month, hoje.day)).order_by('-nr_aprovacoes')][0:100] }
    return render(request, template_name, context)

        #aprovacoes = Aprovacao.objects.filter(usuario=get_object_or_404(Usuario, usuario=self.request.user))
        #return [ { 'publicacao':publicacao, 'aprovacao':aprovacoes.filter(publicacao=publicacao).first() }  for publicacao in query]

