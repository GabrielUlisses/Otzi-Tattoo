from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from tatuador.models import Tatuador, Certificacao
from publicacao.models import Publicacao
from endereco.models import Endereco
from agenda.models import ConfiguracaoAgenda
from usuario.models import Usuario, User

from usuario.forms import UserForm, UsuarioForm, UserEditForm
from tatuador.forms import TatuadorForm, CertificacaoForm, CertificacaoEditForm, BioForm
from endereco.forms import EnderecoForm
from usuario.forms import PedidoOrcamentoForm

from usuario.views import capturar_usuario_sessao, verifica_usuario_sessao
from agenda.views import carregar_configuracao_agenda_por_dia_configurado

@login_required(login_url='pagina_login')
def galeria(request):
    template = "perfil/galeria.html"
    context = {
        "imgs": Publicacao.objects.all().exclude(midia=None).order_by('nr_aprovacoes')[:300]
    } 
    return render(request, template, context)

@login_required(login_url='pagina_login')
def bloquear_tatuador(request, pk):
    """
    View responsável por realizar a inativação da conta de tatuador do usuário em questão.
    """
    try:
        usuario = get_object_or_404(Usuario, id=pk)            
        if usuario.tatuador:
            usuario.tatuador.ativo = False
        usuario.tatuador.save() 
    except:
        messages.error(request, "Esta operação não pode ser executada no momento, tente novamente mais tarde.")
    return redirect('index')

@login_required(login_url='pagina_url')
def reativar_perfil(request, pk):
    """
    View responsável por realizar a reativação da conta de tatuador do usuário em questão.
    """
    try:
        usuario = get_object_or_404(Usuario, id=pk)            
        if usuario.tatuador:
            usuario.tatuador.ativo = True
        usuario.tatuador.save() 
    except:
        messages.error(request, "Esta operação não pode ser executada no momento, tente novamente mais tarde.")
    return redirect('index')

@login_required(login_url='pagina_login')
def bloquear_usuario(request, pk):
    """
    View responsável por realizar o bloqueio do usuário em questão, seu User model do Django e do seu perfil de tatuador (se possuir)
    """
    try:  
        usuario = get_object_or_404(Usuario, id=pk)
        #user = get_object_or_404(User, pk=usuario.usuario.pk)
        usuario.ativo = False
        usuario.usuario.is_active = False
        if usuario.tatuador:
            usuario.tatuador.ativo = False
            usuario.tatuador.save()
        usuario.save() 
        usuario.usuario.save()        
        messages.success(request,"Operação concluida")
    except:
        messages.error(request, "Esta operação não pode ser executada no momento, tente novamente mais tarde.")
        return redirect('index')

@login_required(login_url='pagina_login')
def ver_perfil_usuario(request,pk):
    template = "perfil/usuario.html"
    context = { 'usuario': get_object_or_404(Usuario, id=pk) }
    if not context['usuario'].usuario.is_active:
        raise Http404("Usuário inascessível")
    if context['usuario'].usuario == request.user:
        return redirect('carregar_pagina_usuario')
    context['publicacoes'] = Publicacao.objects.filter(publicante=context['usuario'].usuario)
    return render(request, template,context)

@login_required(login_url='pagina_login')
def ver_perfil_desenhista(request,pk):
    template = "perfil/desenhista.html"
    context = { 'usuario': get_object_or_404(Usuario, id=pk) }
    if not context['usuario'].usuario.is_active:
        raise Http404("Usuário inascessível")
    if context['usuario'].usuario == request.user:
        if get_object_or_404(Usuario,usuario=request.user).desenhista:
            return redirect('carregar_pagina_perfil')
        else:
            messages.warning(request, "Você não possui um perfil de desenhista")
            return redirect('carregar_pagina_perfil')
    if not context['usuario'].desenhista:
        messages.error(request, "Este usuário não possui um perfil de desenhista")
        return redirect('carregar_pagina_perfil')
    context['publicacoes'] = Publicacao.objects.filter(publicante=context['usuario'].usuario)
    return render(request, template,context)

@login_required(login_url='pagina_login')
def ver_perfil_tatuador(request,pk):
    template = "perfil/tatuador/tatuador.html"
    context = { 'usuario': get_object_or_404(Usuario, usuario=get_object_or_404( User, pk=pk ) ) }
    print(context['usuario'])
    if not context['usuario'].usuario.is_active:
        raise Http404("Usuário inacessível")
    if context['usuario'].usuario == request.user:
        if get_object_or_404(Usuario,usuario=request.user).tatuador:
            return redirect('carregar_pagina_perfil_tatuador')
        else:
            messages.warning(request, "Você não possui um perfil de tatuador.")
            return redirect('carregar_pagina_perfil')
    if not context['usuario'].tatuador:
        messages.error(request, "Este usuário não possui um perfil de tatuador")
        return redirect('carregar_pagina_perfil')
    context['pedido_orcamento_form'] = PedidoOrcamentoForm( request.POST or None, request.FILES or None )
    context['pedido_orcamento_form'].initial["usuario"] = get_object_or_404(Usuario, usuario=request.user)
    context['publicacoes'] = Publicacao.objects.filter(publicante=context['usuario'].usuario)
    context['certificados'] = Certificacao.objects.filter(tatuador=context['usuario'].tatuador)
    context['configuracao_agenda'] = carregar_configuracao_agenda_por_dia_configurado(context['usuario'].tatuador)
    return render(request, template, context)

def carregar_certificados_formularios(tatuador):
    """
    Função responsável por carregar todos os certificados de um determinado tatuador, para cada certificado recuperado,
    será devolvido um formulario com os dados respectivos preenchidos para eventual edição.
    """
    certificados = Certificacao.objects.filter(tatuador = tatuador)
    formularios = []
    ret,item = [],{}
    
    for i in certificados:
        item['certificado'] = i
        item['formulario'] = CertificacaoEditForm(instance = i)       
        ret.append(item.copy())     
    return ret

@login_required(login_url='pagina_login')
def carregar_pagina_perfil_tatuador(request):
    """
    View responsável por carregar e renderizar todos os dados relacionados à conta de tatuador do usuário da sessão
    """
    template_name = "perfil/tatuador/perfil.html"
    context = {
        'usuario' : capturar_usuario_sessao(request),
    } 
    if not context['usuario'].usuario.is_active:
        raise Http404("Usuário inacessível")
    context['certificados'] = carregar_certificados_formularios(tatuador = context['usuario'].tatuador_id)
    context['studio'] = Endereco.objects.get( id = context['usuario'].tatuador.endereco_id )
    context['certificado_form'] = CertificacaoForm(request.POST or None )
    context['bio_form'] = BioForm(request.POST or None, instance = context['usuario'].tatuador.bio )
    context['tatuador_form'] = TatuadorForm(instance = context['usuario'].tatuador)
    context['configuracao_agenda'] = carregar_configuracao_agenda_por_dia_configurado(context['usuario'].tatuador)
    context['studio_form'] = EnderecoForm(request.POST or None,instance=context['studio'])

    return render( request, template_name, context )

@login_required(login_url='pagina_login')
def editar_dados_perfil_tatuador(request):
    """
    View responsável por receber e validar os dados de edição do tatuador.
    """
    if request.POST:
        tatuador = get_object_or_404(Tatuador, pk=request.POST.get('tatuador_id'))
        form = TatuadorForm(request.POST, instance = tatuador)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Alterações salvas com sucesso!")
        else:
            messages.error(request,"Dados inválidos")
        return redirect('carregar_pagina_perfil_tatuador')
    return redirect('index')

@login_required(login_url='pagina_login')
def carregar_pagina_perfil(request):
    """
    View responsável por renderizar a página do perfil contendo os dados do usuário
    """
    if verifica_usuario_sessao(request) == 'autenticado':
        usuario = capturar_usuario_sessao(request)
        if usuario: 
            if not usuario.usuario.is_active:
                raise Http404("Usuário inacessível")
            template_name = "perfil/perfil.html"
            context = {
                'user_form': UserEditForm(request.POST or None, instance = usuario.usuario),
                'usuario_form': UsuarioForm(request.POST or None, instance = usuario),
                'usuario': usuario,
                'numero_publicacoes': Publicacao.objects.filter(publicante = usuario.usuario).count(),
                'minhas_publicacoes': Publicacao.objects.filter(publicante = usuario.usuario),
            }
            if not usuario.tatuador:
                context['tatuador_form'] = TatuadorForm(request.POST or None)
                context['endereco_form'] = EnderecoForm(request.POST or None)
            context['desenhistas'] = carregar_publicacoes_por_usuario(Usuario.objects.filter(desenhista=True))
            context['tatuadores'] = carregar_publicacoes_por_usuario(Usuario.objects.extra(where=["tatuador_id is not null"]))
            context['usuarios'] = carregar_publicacoes_por_usuario(Usuario.objects.all())
            context['studios'] = Endereco.objects.all().reverse()[:5]
            context['pedido_orcamento_form'] = PedidoOrcamentoForm( request.POST or None, request.FILES or None)
            context['pedido_orcamento_form'].initial["usuario"] = get_object_or_404(Usuario, usuario=request.user)
        else:
            messages.error(request," Não foi possível recuperar o usuário da sessão.")
            return redirect('index')
    else: 
        messages.error(request,"Realize seu login.")
        return redirect('pagina_login')
    return render(request, template_name, context)

@login_required(login_url='pagina_login')
def editar_dados_perfil(request):
    """
    View responsável por tratar os dados alterados do perfil
    """
    if request.POST:
        usuario = capturar_usuario_sessao(request)
        if not usuario.usuario.is_active:
            raise Http404("Usuário inacessível")
        user_form = UserEditForm(request.POST, request.FILES, instance=usuario.usuario)
        usuario_form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if user_form.is_valid() and usuario_form.is_valid():
            usuario_form.save()
            user_form.save()
            messages.success(request, "Alterações salvas com suceso!")
        else:
            messages.error(request, "Não foi possível registrar as alterações realizadas.")
        return redirect('carregar_pagina_perfil')
    return redirect('index')

@login_required
def request_editar_dados_perfil(request):
    """
    View responsável por renderizar a página do perfil contendo os dados do usuário para edição
    """
    template_name = 'perfil/editar_perfil.html'
    if verifica_usuario_sessao(request) == "autenticado":
        usuario = capturar_usuario_sessao(request)
        if usuario.usuario.is_active:
            raise Http404("Usuário inacessível")
        context = {
            'user_form': UserForm(instance = usuario.usuario),
            'usuario_form': UsuarioForm(instance = usuario)
        }
        return render(request, template_name, context)
    else:
        return redirect('index')

@login_required
def remover_perfil(request, user_pk):
    try:
        usuario = Usuario.objects.get(pk = user_pk)
        usuario.ativo = False
        usuario.usuario.is_active = False
        usuario.save()
        messages.success(request,'Seu perfil foi removido com sucesso...')
    except:
        messages.error(request,'Não foi possível remover o perfil')
    return redirect('index')

def carregar_publicacoes_por_usuario(queryset):
    lista = []
    context = {}
    for item in queryset:      
        context['usuario'] = item 
        context['publicacoes'] = Publicacao.objects.filter(publicante = item.usuario).reverse()[:5]
        lista.append(context.copy())
    return lista

def consultar_perfil(request, pk):
    context = {
        "usuario" : get_object_or_404(Usuario, pk=pk),
    }
    if usuario.usuario.is_active:
        return Http404()
    context["publicacoes"] = Publicacao.objects.filter(usuario = context["usuario"])
