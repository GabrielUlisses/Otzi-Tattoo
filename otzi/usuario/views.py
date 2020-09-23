
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # biblioteca para retornar mensagens
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


from tatuador.models import Tatuador
from publicacao.models import Publicacao
from notificacao.models import TipoNotificacao


from tatuador.forms import TatuadorForm
from endereco.forms import EnderecoForm

from notificacao.views import gerar_notificacao

from .models import *
from .forms import *
from .serializers import UserSerializer, UsuarioSerializer

# #------------------- API --------------------#
class UsuarioAPIView(APIView):
 
    def get(self,request,username=None):
        #objects = Usuario.objects.filter(Q(usuario__username__unaccent__trigram__similar=username) | Q(nome__unaccent__trigram__similar=username)).exclude(usuario = request.user, usuario__is_active = False).reverse()[:5] if username else Usuario.objects.all().exclude(usuario = request.user).reverse()[:5]
        objects = Usuario.objects.filter(Q(usuario__username__icontains=username) | Q(nome__icontains=username)).exclude(usuario = request.user, usuario__is_active = False).reverse()[:5] if username else Usuario.objects.all().exclude(usuario = request.user).reverse()[:5]
        serializer = UsuarioSerializer(objects, many=True)      
        return Response(serializer.data)

class TatuadorAPIView(APIView):
    def get(self, request, username=None):
        objects = Usuario.objects.extra(where=["tatuador_id is not null"]).filter(Q(usuario__username__icontains=username) | Q(nome__icontains=username)).exclude(usuario = request.user, usuario__is_active = False).reverse()[:5] if username else Usuario.objects.extra(where=["tatuador_id is not null"]).exclude(usuario = request.user).reverse()[:5]
        serializer = UsuarioSerializer(objects, many=True)
        return Response(serializer.data)

class DesenhistaAPIView(APIView):
    def get(self, request,username=None):
        objects = Usuario.objects.filter(Q(desenhista = True) & Q(usuario__username__icontains = username) | Q(nome__icontains=username) ).exclude(usuario = request.user, usuario__is_active = False).reverse()[:5] if username else Usuario.objects.filter(desenhista = True).exclude(usuario = request.user).reverse()[:5]
        serializer = UsuarioSerializer(objects, many=True)
        return Response(serializer.data)

#------------------- SESSÃO --------------------#
def capturar_usuario_sessao(request):
    '''
        View responsável por capturar o usuário da sessão (user object) 
        e retornar um objeto do modelo Usuario.
    '''
    user = User.objects.get(username = request.user.username)
    usuario = Usuario.objects.get(usuario = user)
    return usuario

def verifica_usuario_sessao(request):
    """
    View responsável por verificar se há usuário logado na sessão
    """
    if request.user.is_authenticated:
        return "autenticado"
    else:
        return "nao_autenticado"

#------------------- REGISTRO USUARIO --------------------#
def carregar_pagina_cadastro(request):
    """
    View responsável por renderizar a página de cadastro
    """
    template_name = 'login/pagina_cadastro.html'
    context = {
        'user_form' : UserForm(),
        'usuario_form': UsuarioForm(),
    }
    return render(request, template_name, context)

def registrar_usuario(request):
    """
    View responsável por receber os dados submetidos para o cadastro de um novo usuário na plataforma
    """
    user_form = UserForm(request.POST or None, request.FILES or None)
    usuario_form = UsuarioForm(request.POST or None, request.FILES or None)
    template_name = 'login/pagina_cadastro.html'

    if request.POST:
        if user_form.is_valid():
            user_form.clean_password()
            name = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            confirm_password= user_form.cleaned_data['confirm_password']
            email = user_form.cleaned_data['email']
            user = User.objects.create_user(username=name, email=email, password=password)
        else:
            messages.error(request,"Corrija os erros abaixo.")
            context = {
            'user_form' : user_form,
            'usuario_form': usuario_form,
            }
            return render(request, template_name, context)
        if usuario_form.is_valid():
            nome = usuario_form.cleaned_data['nome']
            imagem = usuario_form.cleaned_data['imagem']
            desenhista = usuario_form.cleaned_data['desenhista']
            usuario = Usuario.objects.create(usuario=user, imagem=imagem, desenhista=desenhista, nome=nome)
            if usuario and user:
                user.save()
                usuario.save()
                messages.success(request,'Usuario cadastrado com sucesso!')
                singin(request, name, password)
                return redirect('index')
            else:
                messages.error(request,"Ocorreu um erro durante a realização do cadastro.")
        else:
            messages.error(request,"Corrija os erros abaixo.")
            context = {
            'user_form' : user_form,
            'usuario_form': usuario_form,
            }
            return render(request, template_name, context)
    else:
        context = {
            'user_form' : user_form,
            'usuario_form': usuario_form,
        }
        return render(request, template_name, context)

#------------------- LOGIN LOGOUT --------------------#
def carregar_pagina_login(request):
    """
    View resposável por renderizar a página de login
    """
    template_name = "login/login.html"
    context = {
        'form' : UserForm(request.POST or None)
    }
    #context['form'].fields['username'].initial = request.POST.get('login')
    if verifica_usuario_sessao(request) == "autenticado":
            logout(request)
    return render(request, template_name, context)

def singin(request, username, passwd):
    user = authenticate(request, username=username, password=passwd)
    if user != None:
        login(request,user)
        return True
    else:
        return False

@csrf_protect
def submit_login(request):
    """
    View responsável por validar os dados do login e autenticar o usuário da sessão
    """
    if request.method == 'POST':
        username = request.POST.get('login')
        passwd = request.POST.get('senha')
        if singin(request, username, passwd):
            return redirect('index')
        else:
            messages.error(request,"Credenciais inválidas..")
            return redirect('pagina_login')
    else:
        messages.add_message(request, messages.ERROR,'Credenciais inválidas.' )
        return redirect('pagina_login')

@login_required(login_url='pagina_login')
def singout(request):
    if verifica_usuario_sessao(request) == "autenticado":
        logout(request)
        return redirect('index')
    else:
        messages.INFO(request, 'É necessário estar autenticado para realizar o logout')
        return redirect('index')

#------------------- TESTES --------------------#

@login_required(login_url='pagina_login')
def formulario_pedido_orcamento(request):
    template = "usuario/pedido_orcamento_form.html"
    context = {
        'form' : PedidoOrcamentoForm(request.POST or None, request.FILES or None),
    }
    if request.POST:
        if context["form"].is_valid():
            messages.success(request,"Dados Validados com sucesso!")
        else:
            messages.error(request,"Dados inválidos")
    return render(request,template,context)

@login_required(login_url='pagina_login')
def gerar_pedido_orcamento(request):
    """
    View responsável gerar o pedido de orcamento
    """
    if request.POST:
        form = PedidoOrcamentoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            obj.tatuadores.add( get_object_or_404(Usuario,id=request.POST["usuario_id"]).tatuador )
            obj.save()
            imgs = ""
            if obj.img_1:
                imgs += "<img class='img rounded' src='"+obj.img_1.url+"' width='90' height='90'>"
            if obj.img_2:
                imgs += "<img class='img rounded' src='"+obj.img_2.url+"' width='90' height='90'>"
            if obj.img_3:
                imgs += "<img class='img rounded' src='"+obj.img_3.url+"' width='90' height='90'>"
            gerar_notificacao(
                request.user,
                titulo = "Pedido de orçamento gerado com sucesso!",
                emissor = User.objects.get(username="admin"),
                conteudo = "Gostaríamos de informar que seu pedido de orçamento foi enviado com sucesso para o tatuador <a class='text-info' href='http://127.0.0.1:8000/perfil/tatuador/"+str(obj.tatuadores.first().usuario.usuario.id)+"/'>"+str(obj.tatuadores.first().usuario.nome)+"</a>",
                tipo = TipoNotificacao.objects.get(tipo="Comum")
            )
            gerar_notificacao(
                Usuario.objects.get(id=request.POST["usuario_id"]).usuario,
                titulo = "Você acaba de receber um novo pedido de orçamento!",
                emissor = request.user,
                conteudo = "O usuário <a class='text-info' href='http://127.0.0.1:8000/perfil/usuario/"+str(request.user.id)+"/'>"+str(request.user.username)+"</a> lhe enviou um pedido de orçamento <br><br>"
                +"<h6><strong>"+form.cleaned_data["titulo"]+"</strong></h6>"
                +"<p><strong>"+form.cleaned_data['texto_receptivo']+"</strong></p>"
                +"<p><strong> Parte do corpo: "+form.cleaned_data['parte_corpo']+" </strong></p>"
                +"<p><strong> Tamanho: "+form.cleaned_data['tamanho']+" </strong></p>"
                +"<p><strong> Descrição Complementar: "+form.cleaned_data['texto_complementar']+" </strong></p>"
                +"<p><strong> Valor esperado: R$ "+str(form.cleaned_data['preco_esperado'])+" </strong></p>"
                +imgs            
                ,tipo = TipoNotificacao.objects.get(tipo="Comum")
            )
            messages.success(request, "Pedido de orçamento gerado com sucesso!")
            return redirect("carregar_pagina_perfil")
        messages.error(request, "Não foi possível gerar pedido de orçamento")
        return redirect("carregar_pagina_perfil")
    return redirect("index")


