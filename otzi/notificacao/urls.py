from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register('notificacao-usuarios', NotificacaoUsuarioViewSet)
router.register('notificacoes', NotificacaoViewSet)
#router.register(r'notificacoes_enviadas',NotificacaoEnviadaViewSet, basename="notificacoes_enviadas_serializer")
#router.register(r'notificacoes_recebidas',NotificacaoRecebidaViewSet, basename="notificacoes_recebidas_serializer")
#router.register(r'notificacoes', NotificacaoViewSet, basename='notificacoes')

urlpatterns = [
   path('notificacoes/', login_required( function=carregar_notificacoes, login_url="pagina_login" ), name="notificacoes" ),
   path('remover/<int:not_pk>/', login_required( function=remover_notificacao, login_url="pagina_login" ), name="remover_notificacao"),
   path('notificacao/set_lida/<int:user_pk>/<int:not_pk>/',login_required( function=NotificacaoSetLidoApiView.as_view(), login_url="pagina_login" ) , name="notificacao_set_lida")
]
