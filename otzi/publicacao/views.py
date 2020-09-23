from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView, Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from usuario.models import *

from .forms import *
from .models import *
from .serializers import PublicacaoSerializer, AprovacaoSerializer

#TODO: LISTAR PUBLICAÇÕES COM MAIS APROVAÇÕES


class PublicacaoUsuarioListView(ListView):
    models = Publicacao
    template_name = 'publicacao/publicacoes.html'
    context_object_name = 'publicacoes'
    paginate_by = 20

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        queryset = Publicacao.objects.filter(publicante=user, ativo=True)
        return [ { 'publicacao' : publicacao } for publicacao in queryset ]    

class PublicacaoListView(ListView):
    models = Publicacao
    template_name = 'publicacao/publicacoes.html'
    queryset = Publicacao.objects.filter(ativo=True)
    context_object_name = 'publicacoes'
    paginate_by = 20

    def get_queryset(self):
        query = super().get_queryset()
        aprovacoes = Aprovacao.objects.filter(usuario=get_object_or_404(Usuario, usuario=self.request.user))
        return [ { 'publicacao':publicacao, 'aprovacao':aprovacoes.filter(publicacao=publicacao).first() }  for publicacao in query]

class PublicacaoDetailView(DetailView):
    models = Publicacao
    template_name = 'publicacao/publicacao.html'
    context_object_name = 'publicacao'
    queryset = Publicacao.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['usuario_sessao'] = self.request.user
        context['aprovacao'] = Aprovacao.objects.filter(publicacao=context['publicacao'],usuario=Usuario.objects.filter(usuario=self.request.user).first())
        return context

@login_required(login_url='pagina_login')
def criar_publicacao(request):
    '''
    View Responsável por receber e validar os dados submetidos para o cadastro de uma nova publicação
    '''
    if request.POST: 
        print(request.POST.keys())
        # RECEIVE DATA
        if request.POST['titulo']:
            titulo = request.POST['titulo']
            user = User.objects.get(username = request.user)
            if request.POST['conteudo'] and request.FILES['midia']:
                conteudo = request.POST['conteudo']
                imagem = request.FILES['midia']
                ret = criar(request, titulo, user, conteudo, imagem)
            elif request.POST['conteudo']:
                conteudo = request.POST['conteudo']
                ret = criar(request, titulo, user, conteudo)
            elif request.FILES['midia']:
                imagem = request.FILES['midia']
                ret = criar(request, titulo, user, None, imagem)
            else:
                ret = criar(request, titulo, user)
            if ret:
                if ret == "sucesso":
                    return redirect('../../')
                else:
                    return redirect('../')
        else:
            messages.success(request,'A publicação precisa ter um título.')
            return redirect('../')
    else:
        context = {
            'form' : PublicacaoForm(),
        }
        template_name = 'publicacao/publicacao_form.html'
        return render(request, template_name, context)

def criar(request, titulo, user, conteudo = None, imagem = None):
    try:
        # CREATE A PUBLICACAO OBJECT
        pub = Publicacao.objects.create( 
            titulo = titulo,
            conteudo = conteudo,
            publicante = user,
            midia = imagem
        )
        pub.aprovacoes()
        messages.success(request,'Publicação criada com sucesso.')
        return "sucesso"
    except:
        messages.error(request, 'Ocorreu um erro ao criar uma nova publicação')
        return "erro"

class PublicacaoUpdateView(UpdateView):
    model = Publicacao
    template_name = 'publicacao/publicacao_form.html'
    fields = ['titulo','conteudo','midia']
    success_url = reverse_lazy('publicacoes')

class PublicacaoDeleteView(DeleteView):
    model = Publicacao
    template_name = 'publicacao/publicacao.html'
    context_object_name = 'publicacao'
    success_url = reverse_lazy('index')

@login_required(login_url='pagina_login')
def remover_publicacao(request, pk):
    try:
        pub = Publicacao.objects.get(id = pk)
        pub.ativo = False
        pub.save()
        messages.success(request,'Publicação removida com sucesso.')
        return redirect("publicacoes")
    except:
        messages.error(request, 'Não foi possível remover esta publicação.')
        return redirect('publicacoes')

#################### APROVAÇÔES ####################

class AprovacaoViewSet(viewsets.ModelViewSet):
    serializer_class = AprovacaoSerializer

    @action(detail=True, methods=['GET'])
    def aprovar_publicacao(self, request, pub_id):
        ap = Aprovacao.objects.create(publicacao=get_object_or_404(Publicacao, id=pub_id), usuario=get_object_or_404(Usuario, usuario=request.user))
        ap.save()
        ap.publicacao.aprovacoes()     
        serializer = AprovacaoSerializer(ap, many=False)
        return Response(serializer.data)

    @action(detail=True, method=['GET'])
    def cancelar_aprovacao(self, request, pub_id):
        ap = get_object_or_404(Aprovacao, publicacao=get_object_or_404(Publicacao, id=pub_id), usuario=get_object_or_404(Usuario, usuario=request.user))
        publicacao = ap.publicacao
        ap.delete()
        publicacao.aprovacoes()
        serializer = PublicacaoSerializer(publicacao)
        return Response(serializer.data)




