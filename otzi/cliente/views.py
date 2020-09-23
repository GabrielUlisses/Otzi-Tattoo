from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# def get_tatuadorModel_full():
#     """
#     Function responsável pela recuperação completa dos dados associados ao tatuador (usuario,especializacao) que não são carregados por padrão
#     """
#     lista = Usuario.objects.all()
#     ret = []
#     for i in lista:
#         if i.especializacao:
#             if i.especializacao.tatuador:
#                 ret.append({'usuario':i,'tatuador':Tatuador.objects.get(especializacao = i.especializacao)})
#     print(ret)
#     return ret

# def get_desenhistas():
#     desenhistas = Usuario.objects.filter(desenhista = True)
#     ret = []
#     for i in desenhistas:
#         item = {'desenhista':i,'pubs':Publicacao.objects.filter(publicante = i.usuario)[:5]}
#         ret.append(item.copy())
#     return ret



