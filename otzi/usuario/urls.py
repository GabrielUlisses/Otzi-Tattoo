from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [
    path('', carregar_pagina_login, name='pagina_login'),
    path('pagina_registro/', carregar_pagina_cadastro, name="pagina_registro"),
    
    path('submit/', submit_login, name="submit_login"),
    path('registro/', registrar_usuario, name="submit_registro"),
    path('logout/', singout, name="logout"),

    path('pedido-orcamento/', gerar_pedido_orcamento, name="gerar_pedido_orcamento"),

    # ---------- API ---------- #

    path('api/v1/usuarios/', UsuarioAPIView.as_view(), name="get_usuarios"),
    path('api/v1/usuarios/<str:username>/', UsuarioAPIView.as_view(), name="get_usuarios"),

    path('api/v1/tatuadores/', TatuadorAPIView.as_view(),  name="get_tatuadores"),
    path('api/v1/tatuadores/<str:username>/', TatuadorAPIView.as_view(),  name="get_tatuadores"),

    path('api/v1/desenhistas/', DesenhistaAPIView.as_view(),  name="get_desenhistas"),
    path('api/v1/desenhistas/<str:username>/', DesenhistaAPIView.as_view(),  name="get_desenhistas"),
]
