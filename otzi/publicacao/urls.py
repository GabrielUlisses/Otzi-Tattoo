from django.urls import path
from .views import *

urlpatterns = [
    path('criar/', criar_publicacao, name="criar_publicacao"),
    path('editar/<int:pk>/', login_required(function=PublicacaoUpdateView.as_view(), login_url='pagina_login'), name="editar_publicacao"),
    path('remover/<int:pk>/', remover_publicacao , name="remover_publicacao"),
    path('visualizar/<int:pk>/', login_required(function=PublicacaoDetailView.as_view(), login_url='pagina_login'), name="visualizar_publicacao"),
    
    path('minhas-publicacoes/',login_required(function=PublicacaoUsuarioListView.as_view(), login_url='pagina_login'),name='publicacoes_usuario'),
    path('', login_required(function=PublicacaoListView.as_view(), login_url='pagina_login'), name='publicacoes'),
    
    path('api/v1/aprovar/<str:pub_id>/', login_required(function=AprovacaoViewSet.as_view({'get':'aprovar_publicacao'}), login_url='pagina_login') , name="aprovar_publicacao"),
    path('api/v1/desaprovar/<str:pub_id>/', login_required(function=AprovacaoViewSet.as_view({'get':'cancelar_aprovacao'}), login_url='pagina_login'), name="desaprovar_publicacao"),
]
