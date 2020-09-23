
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from notificacao.urls import router

urlpatterns = [
    path('api/v1/', include(router.urls)),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('agenda/', include('agenda.urls'), name='agenda'),
    path('chat/', include('chat.urls'), name='chat'),
    #path('cliente/', include('cliente.urls'), name='cliente'),
    path('denuncia/', include('denuncia.urls'), name='denuncia'),
    path('endereco/', include('endereco.urls'), name='endereco'),
    path('horario/', include('horario.urls'), name='horario'),
    path('notificacao/', include('notificacao.urls'), name='notificacao'),
    path('perfil/', include('perfil.urls'), name='perfil'),
    path('publicacao/', include('publicacao.urls'), name='publicacao'),
    path('tatuador/', include('tatuador.urls'), name='tatuador'),
    path('usuario/', include('usuario.urls'), name='usuario'),
    path('', include('core.urls')),
] 

urlpatterns = urlpatterns + static( settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static( settings.STATIC_URL, document_root= settings.STATIC_ROOT)
