from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import TatuadorSerializer

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404

from usuario.views import capturar_usuario_sessao
from agenda.views import carregar_configuracao_agenda_por_dia_configurado

from usuario.models import Usuario
from publicacao.models import Publicacao
from tatuador.models import *
from agenda.models import Agenda, ConfiguracaoAgenda

from endereco.forms import EnderecoForm

from perfil.views import carregar_pagina_perfil

from .forms import *
from .models import *
from django.http import HttpResponseRedirect

def formulario_tatuador(request):
    """
    View responsável por carregar o formulário do tatuador
    """
    template = "tatuador/formulario.html"
    form = TatuadorForm(request.POST or None, request.FILES or None)
    context = {
        'form' : form
    }
    if request.POST:  
        if form.is_valid():
            messages.success(request, "Dados válidados com sucesso.")
        else:
            messages.error(request, "Dados inválidos.")
        return render(request, template, context)
    else:
        return render(request, template, context)

def formulario_certificacao(request):
    """
    View responsável por carregar o formulário de certificação
    """
    template = "tatuador/certificacao_form.html"
    form = CertificacaoForm(request.POST or None, request.FILES or None)
    context = {
        'form' : form
    }
    if request.POST:  
        if form.is_valid():
            messages.success(request, "Dados válidados com sucesso.")
        else:
            messages.error(request, "Dados inválidos.")
        return render(request, template, context)
    else:
        return render(request, template, context)

def formulario_bio(request):
    """
    View responsável por carregar o formulário de Biografia do tatuador.
    """
    template = "tatuador/bio_form.html"
    form = BioForm(request.POST or None)
    context = {
        'form' : form
    }
    if request.POST:  
        if form.is_valid():
            messages.success(request, "Dados válidados com sucesso.")
        else:
            messages.error(request, "Dados inválidos.")
        return render(request, template, context)
    else:
        return render(request, template, context)

# ---------- TATUADOR ---------- #
@login_required(login_url='pagina_login')
def request_registrar_tatuador(request):
    """
    View responsável por carregar e renderizar o formulário de registro de tatuador.
    """
    template_name = "perfil/tatuador/pagina_registro.html"
    context = {}
    context['tatuador_form'] = TatuadorForm(request.POST or None)
    context['endereco_form'] = EnderecoForm(request.POST or None)

    return render(request, template_name, context)

@login_required(login_url='pagina_login')
def registrar_tatuador(request):
    """
    View responsável por renderizar e validar os formulários de especializacao, endereço e tatuador.
    """
    if request.POST:
        
        formulario_tatuador = TatuadorForm(request.POST or None, request.FILES or None)
        formulario_endereco = EnderecoForm(request.POST or None)
        
        # SE TUDO ESTIVER OK INICIA O CADASTRO
        if formulario_tatuador.is_valid() and formulario_endereco.is_valid():          
            tatuador = Tatuador.objects.create(                   
                    cpf = formulario_tatuador.cleaned_data['cpf'],
                    telefone = formulario_tatuador.cleaned_data['telefone'],
                    wathsapp = formulario_tatuador.cleaned_data['wathsapp'],
                    facebook = formulario_tatuador.cleaned_data['facebook'],
                    instagram = formulario_tatuador.cleaned_data['instagram'],
                    site_pessoal = formulario_tatuador.cleaned_data['site_pessoal'],
                    endereco = formulario_endereco.save(),
                    agenda = Agenda.objects.create()
                )
            tatuador.save()

            usuario = Usuario.objects.get(usuario = request.user)
            usuario.tatuador = tatuador
            usuario.save()
            messages.success(request,"Registro realizado com sucesso!")
            return HttpResponseRedirect(reverse('carregar_pagina_perfil'))
        else:
            messages.error(request, 'Corrija os campos inválidos.')
            return HttpResponseRedirect(reverse('request_registrar_tatuador'))
    else:
        return HttpResponseRedirect(reverse('request_registrar_tatuador'))

# ---------- CERTIFICADO ---------- #

@login_required(login_url='pagina_login')
def registrar_certificado(request):
    if request.POST:
        form = CertificacaoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            #try:
                cert = Certificacao.objects.create(
                    tatuador = capturar_usuario_sessao(request).tatuador,
                    data = form.cleaned_data['data'],
                    titulo = form.cleaned_data['titulo'],
                    descricao = form.cleaned_data['descricao'],
                    codigo = form.cleaned_data['codigo'],
                    imagem = form.cleaned_data['imagem'],
                )
                cert.save()
                messages.success(request,"Certificação registrada com sucesso.")
            #except:
                #messages.error(request,"Ocorreu um erro durante o registro da certificação. Tente novamente mais tarde.")
        else:
            messages.error(request,"Corrija os erros abaixo.")
    return redirect('carregar_pagina_perfil_tatuador')

def carregar_certificados_formulario(tatuador):
    certificados = Certificacao.objects.filter(tatuador = tatuador)
    formularios, context = [],{}
    ret,item = [],{}
    
    for i in certificados:
        item['certificado'] = i
        item['formulario'] = CertificacaoEditForm(instance = i)       
        ret.append(item.copy())
       
    return ret

def editar_certificado(request):
    """
    View responsável por receber, validar e salvar as alterações pertinentes realizadas sobre as informações de um certificado
    """
    form = CertificacaoEditForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            certificado = Certificacao.objects.get(id = request.POST["certificado_id"])
            certificado.data = form.cleaned_data['data'] 
            certificado.titulo = form.cleaned_data['titulo']
            certificado.descricao = form.cleaned_data['descricao']
            certificado.codigo = form.cleaned_data['codigo']

            certificado.save()
            messages.success(request, "Alterações salvas com sucesso!")
        else:
            messages.error(request, "Corrija os erros do formulário.")
    return redirect("carregar_pagina_perfil_tatuador")

def remover_certificado(request):
    if request.POST:
        try:
            certificado = Certificacao.objects.get(id = request.POST['certificado_id'])
            certificado.ativo = False
            certificado.save()
            messages.success(request, "Remoção concluída!")
        except:
            messages.error(request, "Ocorreu um erro durante a remoção, operação cancelada..")
    return redirect("carregar_pagina_perfil_tatuador")

# ---------- BIO --------- #
@login_required(login_url='pagina_login')
def registrar_bio(request):
    if request.POST:
        form = BioForm(request.POST or None)
        if form.is_valid():
            #try:
                bio = Bio(
                    apresentacao = form.cleaned_data['apresentacao'],
                    conteudo = form.cleaned_data['conteudo'],
                )
                tatuador = get_object_or_404(Tatuador, id = request.POST['tatuador_id'])
                bio.save()
                tatuador.bio = bio
                tatuador.save()
                print(tatuador.bio.apresentacao)
                #tatuador.bio_id = tatuador.bio.id
                
                
            #    messages.success(request,"Biografia registrada com sucesso.")
            #except:
            #    messages.error(request,"Ocorreu um erro durante o registro da biografia. Tente novamente mais tarde.")
        else:
            messages.error(request,"Corrija os erros abaixo.")
    return redirect('carregar_pagina_perfil_tatuador')

@login_required(login_url='pagina_login')
def editar_bio(request):
    """
    View responsável por carregar e validar o formulario de edição de Bio.
    """
    form = BioForm(request.POST or None)
    if request.POST:
        if form.is_valid():            
            bio = Bio.objects.get(id = request.POST['bio_id'])
            bio.apresentacao = form.cleaned_data['apresentacao']
            bio.conteudo = form.cleaned_data['conteudo']
            bio.save()  
            messages.success(request, "Alterações salvas com sucesso!")
        else:
            messages.error(request, "Corrija os dados do formulario.")
    return redirect("carregar_pagina_perfil_tatuador")

# ---------- API ---------- #
def tatuador_list_by_name(request, nome):
    if request.method == 'GET':     
        lista = Tatuador.objects.filter(usuario__nome__icontains=nome)[0:5]
        serializer = TatuadorSerializer(lista, many=True)
        return JsonResponse(serializer.data,safe=False)
    return HttpResponse(status=404)

def tatuador_list_by_city(request, cidade=None):
    if request.method == 'GET':
        lista = Tatuador.objects.filter(endereco__cidade__icontains=cidade)[0:5]
        serializer = TatuadorSerializer(lista,many=True)
        return JsonResponse(serializer.data, safe=False)
    return HttpResponse(status=404)

def tatuador_list(request):
    if request.method == 'GET':
        lista = Tatuador.objects.all()[0:5]
        serializer = TatuadorSerializer(lista,many=True)
        return JsonResponse(serializer.data,safe=False)
    return HttpResponse(status=404)

