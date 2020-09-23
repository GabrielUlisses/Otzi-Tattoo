from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

from .forms import *
from .models import *


########## CONFIGURACAO AGENDA ##########

@login_required(login_url='pagina_login')
def formulario_configuracao_agenda(request):
    template = "agenda/configuracao_form.html"
    request.POST['dia'] = "segunda"
    form = ConfiguracaoAgendaForm(request.POST or None)
    agenda = Agenda.objects.get(tatuador = request.session['id_tatuador'])
    context = {
        'form': form
    }
    print('\n{0} {1}\n'.format(dir(form.initial),form.initial.keys()))
    if request.POST:
        if form.is_valid():
            try:
                messages.success(request, "Dados validados com sucesso!")
                conf = ConfiguracaoAgenda.objects.create(
                    agenda = agenda,
                    dia = form.cleaned_data['dia'],
                    horario_inicio = form.cleaned_data['horario_inicio'],
                    horario_termino = form.cleaned_data['horario_termino'],
                    horario_inicio_almoco = form.cleaned_data['horario_inicio_almoco'],
                    horario_termino_almoco = form.cleaned_data['horario_termino_almoco'],
                )
                conf.save()
            except IntegrityError:
                messages.error(request, "Não é possível registrar duas configurações para um mesmo dia.")
            except:
                messages.error(request, "Ocorreu um erro durante o registro dos dados, tente novamente mais tarde.")
        else:
            messages.error(request, "Corrija os erros abaixo.")
    
    return render(request, template, context)

def carregar_configuracao_agenda_por_dia_configurado(tatuador):
    context = {}
    conf = ConfiguracaoAgenda.objects.filter(agenda = tatuador.agenda)
    for i in conf:
        if i.dia == "segunda":
            context['segunda'] = i
        elif i.dia == "terca":
            context['terca'] = i
        elif i.dia == "quarta":
            context['quarta'] = i
        elif i.dia == "quinta":
            context['quinta'] = i
        elif i.dia == "sexta":
            context['sexta'] = i
        elif i.dia == "sabado":
            context['sabado'] = i
        elif i.dia == "domingo":
            context['domingo'] = i
        elif i.dia == "feriado_religioso":
            context['feriado_religioso'] = i
    return context

@login_required(login_url='pagina_login')
def request_editar_configuracao_agenda(request):
    """
    View responsável por carregar o formulário de edição com os dados preenchidos,
    espera como parâmetro o id do objeto à ser alterado, o mesmo deve ser submetido por meio do método POST
    """
    if request.POST:
        template = "agenda/configuracao_edicao_form.html"
        conf = ConfiguracaoAgenda.objects.get(id = request.POST['configuracao_agenda_id'])
        form = ConfiguracaoAgendaForm(instance = conf)
        # Inserção de atributos dinâmicos para o template #
        form.fields['dia'].widget.attrs['disabled'] = 'disabled'  

        # form.fields['dia'].widget.attrs['title'] = "Dia"
        # form.fields['dia'].widget.attrs['data-content'] = "Esse campo campo não será submetido para edição, alterá-lo não surtirá efeito algum."
        # form.fields['dia'].widget.attrs['data-toggle'] = "popover"
        # form.fields['dia'].widget.attrs['data-trigger'] = "hover"
        # form.fields['dia'].widget.attrs['id'] = "dia"

        context = {
            'form': form,
            'configuracao': conf,
        }
        return render(request, template, context)
    else:
        return redirect('index')

@login_required(login_url='pagina_login')
def editar_configuracao_agenda(request):
    """
    View responsável por gravar as alterações vindas do formulário de edição.
    """
    template = "agenda/configuracao_edicao_form.html"
    form = ConfiguracaoAgendaForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            conf = ConfiguracaoAgenda.objects.get(id = request.POST['configuracao_agenda_id'])
            conf.horario_inicio = form.cleaned_data['horario_inicio']
            conf.horario_termino = form.cleaned_data['horario_termino']
            conf.horario_inicio_almoco = form.cleaned_data['horario_inicio_almoco']
            conf.horario_inicio_almoco = form.cleaned_data['horario_inicio_almoco']
            conf.save()
            messages.success(request, "Dados alterados com sucesso!")
            return redirect('carregar_pagina_perfil_tatuador')
        else:
            messages.error(request, "Não foi possível salvar as alterações.")
            context = {
                'form': form,
                'configuracao': ConfiguracaoAgenda.objects.get(id = request.POST['configuracao_agenda_id']),
            }
            return render(request, template,context)
    else:
        return redirect('index')

@login_required(login_url='pagina_login')
def request_configurar_configuracao_agenda(request):
    template = "agenda/configuracao_form.html"
    form = ConfiguracaoAgendaForm()
    dia = request.POST['dia']
    form.initial['dia'] = dia
    form.fields['dia'].widget.attrs['disabled'] = 'disabled'
    agenda = Agenda.objects.get(id = request.POST['agenda_id']) 
    context = {
        'form': form,
        'agenda': agenda,
        'dia': dia
    }
    return render(request, template, context)

@login_required(login_url='pagina_login')
def configurar_configuracao_agenda(request):
    form = ConfiguracaoAgendaForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            try:             
                conf = ConfiguracaoAgenda.objects.create(
                    agenda = Agenda.objects.get(id = request.POST['agenda_id']),
                    dia = request.POST.get('dia', None),
                    horario_inicio = form.cleaned_data['horario_inicio'],
                    horario_termino = form.cleaned_data['horario_termino'],
                    horario_inicio_almoco = form.cleaned_data['horario_inicio_almoco'],
                    horario_termino_almoco = form.cleaned_data['horario_termino_almoco'],
                )
                conf.save()
                messages.success(request, "Configuração realizada com sucesso!")
                return redirect('carregar_pagina_perfil_tatuador')
            except IntegrityError:
                messages.error(request, "Não é possível registrar duas configurações para um mesmo dia.")
            except:
                messages.error(request, "Ocorreu um erro durante o registro dos dados, tente novamente mais tarde.")
        else:
            messages.error(request, "Corrija os erros do formulário.")
    return request_configurar_configuracao_agenda(request)

@login_required(login_url='pagina_login')
def remover_configuracao_agenda(request):
    if request.POST: 
        if 'configuracao_agenda_id' in request.POST: 
            try:
                conf = ConfiguracaoAgenda.objects.get(id = request.POST['configuracao_agenda_id'])
                conf.delete()
                messages.success(request, "Remoção concluída.")
            except:
                messages.error(request, "Ocorreu um erro durante a remoção.")
        else:
            messages.alert(request,"Não foi possível concluir a remoção, tente novamente mais tarde.")
        return redirect('carregar_pagina_perfil_tatuador')
    else:
        return redirect('index')








