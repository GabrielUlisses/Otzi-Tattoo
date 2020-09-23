from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime as dt

from publicacao.models import Publicacao
from notificacao.views import gerar_notificacao
from notificacao.models import TipoNotificacao

from .models import DenunciaUsuario, DenunciaPublicacao, TipoDenuncia
from .forms import DenunciaPublicacaoForm, DenunciaUsuarioForm


@login_required(login_url="index")
def request_denunciar_publicacao(request, pub_id):
    """
    View responsável tratar a requisição de denúncia contra uma publicação
    """
    form = DenunciaPublicacaoForm(request.POST or None)
    publicacao = Publicacao.objects.get(id = pub_id)
    form.fields['publicacao'].initial = publicacao
    form.fields['denunciante'].initial = request.user
    context = {
        'form': form,
        'publicacao':publicacao
    }
    template_name = "denuncia/denunciaPub_form.html"
    return render(request, template_name, context)

@login_required(login_url="index")
def denunciar_publicacao(request):
    """
    View responsável por receber e validar os dados pertinentes,
    para o registro de uma denúncia contra uma publicação e consequentemente, 
    gerar uma mensagem notificadora para os usuários envolvidos.
    """
    if request.POST:
        form = DenunciaPublicacaoForm(request.POST or None)
        if form.is_valid():
            form.save()
            publicacao = Publicacao.objects.get(id = request.POST['publicacao'])
            gerar_notificacao(
                request.user, 
                titulo="Registro de Denúncia",
                emissor=User.objects.get(username='admin'),
                conteudo=" Nós da aministração gostariamos de comunicar o bem sucedido registro da sua denúncia contra a publicacao"
                +"<a class='text-info' href=\"http://127.0.0.1:8000/publicacao/visualizar/"+str(publicacao.id)+"/\">"+publicacao.titulo+"</a> pertencente ao usuário <a class='text-info' href=\"http://127.0.0.1:8000/perfil/usuario/"+str(publicacao.publicante.id)+"/\">"+publicacao.publicante.username+"</a> nesta data de "+dt.now().strftime("%m/%d/%Y, %H:%M")
                +". Agradecemos vossa colaboração com a manutenção da ordem dentro do nosso sistema,"
                "vamos averiguar as circunstâncias do ocorrido e tomar as medidas cabíveis. <br><br>Atenciosamente: Administração",
                tipo=TipoNotificacao.objects.get(tipo='Comum')
            )
            gerar_notificacao(
                publicacao.publicante,
                titulo="Aviso de denúncia",
                emissor=User.objects.get(username='admin'),
                conteudo="Nós da aministração gostariamos de informar que uma denúncia foi registrada contra a sua publicaçao "+
                "<a class='text-info' href=\"http://127.0.0.1:8000/publicacao/visualizar/"+str(publicacao.id)+"/\">"+publicacao.titulo+"</a> por \""+form.cleaned_data['tipo'].tipo+"\" na data de "+dt.now().strftime("%m/%d/%Y, %H:%M")+". Fique atento a sua postura e comportamento enquanto usuário da plataforma,"
                 +"estaremos averiguando melhor as circunstâncias do ocorrido para tomar as medidas cabíveis.. <br><br> Atenciosamente: Administração",
                tipo=TipoNotificacao.objects.get(tipo="Denuncia")
                )
            messages.add_message(request,messages.SUCCESS,"Sua denúncia foi registrada com sucesso")
            return redirect('index')
        else:
            messages.add_message(request,messages.ERROR,'Ocorreu um erro durante o registro da denúnica...')    
    return request_denunciar_publicacao(request)

@login_required(login_url="index")
def request_denunciar_usuario(request,usuario_id):
    template = "denuncia/denunciaUsr_form.html"
    form = DenunciaUsuarioForm(request.POST or None)
    form.fields['denunciante'].initial = request.user
    form.fields['denunciado'].initial = User.objects.get(id = usuario_id)
    context = {
        "form": form
    }
    return render(request, template, context)

@login_required(login_url="index")
def denunciar_usuario(request):
    if request.POST: 
        print(f"\n{request.POST}\n")
        form = DenunciaUsuarioForm(request.POST or None)
        if form.is_valid():
            form.save()
            denunciado = User.objects.get(id = form.cleaned_data['denunciado'].id)
            gerar_notificacao(
                    request.user,
                    titulo = "Registro de Denúncia",
                    emissor = User.objects.get(username="admin"),
                    conteudo = " Nós da aministração gostariamos de comunicar o bem sucedido registro da sua denúncia contra o usuário"
                    +"<a class='text-info' href=\"http://127.0.0.1:8000/perfil/usuario/"+str(denunciado.id)+"/\">"+denunciado.username+"</a> nesta data de "+dt.now().strftime("%m/%d/%Y, %H:%M")
                    +". Agradecemos vossa colaboração com a manutenção da ordem dentro do nosso sistema,"
                    "vamos averiguar as circunstâncias do ocorrido e tomar as medidas cabíveis. <br><br>Atenciosamente: Administração\n Passar bem.",
                    tipo = TipoNotificacao.objects.get(tipo='Comum'),
            )
            gerar_notificacao(
                    denunciado,
                    titulo="Aviso de denúncia",
                    emissor=User.objects.get(username='admin'),
                    conteudo="Nós da aministração gostariamos de informar que uma denúncia foi registrada contra você por \""+form.cleaned_data['tipo'].tipo+"\""+
                    "na data de "+dt.now().strftime("%m/%d/%Y, %H:%M")+". Fique atento a sua postura e comportamento enquanto usuário do sistema,"
                     +"estaremos averiguando melhor as circunstâncias do ocorrido para tomar as medidas cabíveis.. \n Atenciosamente: Administração",
                    tipo=TipoNotificacao.objects.get(tipo="Denuncia")
            )
            messages.success(request, "Denúncia registrada com sucesso!")
            return redirect("publicacoes")
        messages.error(request, "Ocorreu um erro durante o registro da denúncia")             
        return redirect("publicacoes")
    return redirect("index")