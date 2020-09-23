from django.urls import path
from .views import carregar_pagina_perfil, request_editar_dados_perfil, editar_dados_perfil, carregar_pagina_perfil_tatuador
from .views import editar_dados_perfil_tatuador, ver_perfil_tatuador, ver_perfil_usuario, ver_perfil_desenhista
from .views import bloquear_tatuador, bloquear_usuario
from .views import galeria

urlpatterns = [
    
    path('', carregar_pagina_perfil, name="carregar_pagina_perfil"),
    path('editar/',editar_dados_perfil,name="editar_dados_perfil"),
    
    path('tatuador/', carregar_pagina_perfil_tatuador, name="carregar_pagina_perfil_tatuador"),
    path('tatuador/editar/', editar_dados_perfil_tatuador, name="editar_dados_perfil_tatuador"),

    path('desenhista/<int:pk>/', ver_perfil_desenhista, name="ver_perfil_desenhista"),
    path('usuario/<int:pk>/', ver_perfil_usuario, name="ver_perfil_usuario"),
    path('tatuador/<int:pk>/',ver_perfil_tatuador, name="ver_perfil_tatuador"),

    path('bloquear/usuario/<int:pk>/', bloquear_usuario, name="bloquear_usuario"),
    path('bloquear/tatuador/<int:pk>/', bloquear_tatuador, name="bloquear_tatuador"),

    path('galeria/',galeria, name="galeria" )
]
