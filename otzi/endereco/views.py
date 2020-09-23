from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.validators import ValidationError
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from tatuador.models import Tatuador
from usuario.models import Usuario

from .models import *
from .forms import *
from .serializers import EnderecoSerializer


def formulario(request):
    template = 'endereco/formulario.html'
    if request.POST:
        form = EnderecoForm(request.POST or None)
        if form.is_valid():
            form.save()
            context = {
                'form' : form
            }
            messages.success(request,"Endereço cadastrado com sucesso.")
            return render(request, template, context)
        else:
            context = {
                'form' : form
            }
            return render(request, template, context)
    context = {
        'form' : EnderecoForm()
    }
    return render(request, template, context)

class StudioApiView(APIView):

    def get(self, request, param = None):   
        user = get_object_or_404(Usuario, usuario=request.user)
        if user.tatuador:
            objects = Endereco.objects.filter( Q(cidade__icontains=param) | Q(bairro__icontains=param) | Q(cep__icontains=param)).exclude(id=user.tatuador.endereco.id).reverse()[:5] if param else Endereco.objects.all().order_by("data_criacao").exclude(id=user.tatuador.endereco.id)[:5]     
        else:
            objects = Endereco.objects.filter( Q(cidade__icontains=param) | Q(bairro__icontains=param) | Q(cep__icontains=param)).reverse()[:5] if param else Endereco.objects.all().order_by("data_criacao")[:5]     
        serializer = EnderecoSerializer(objects, many=True)
        return Response(serializer.data)

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

@login_required(login_url='pagina_login')
def editar_dados_studio(request):
    if request.POST:
        endereco = get_object_or_404(Endereco, pk = request.POST.get("studio_id"))
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            messages.success(request, "Alterações salvas com sucesso!")
        else:
            messages.error(request, "Não foi possível salvar as alterações...")
        return redirect('carregar_pagina_perfil_tatuador')
    return redirect('index')

@login_required(login_url='pagina_login')
def ver_studio(request,pk):
    template = "perfil/usuario.html"
    context = {
        'endereco': Endereco.objects.get(id=pk),
        'tatuador': Tatuador.objects.filter(endereco_id = pk)
    } 
    return render(request, template, context)
