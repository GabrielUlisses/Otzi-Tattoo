from django.urls import path
from .views import  registrar_tatuador, editar_certificado, registrar_certificado, remover_certificado, editar_bio
from .views import request_registrar_tatuador, registrar_bio

from .views import tatuador_list, tatuador_list_by_city, tatuador_list_by_name

urlpatterns = [
    # ---------- TATUADOR ---------- #
    path('registrar/', registrar_tatuador, name="registrar_tatuador" ),
    path("registro/", request_registrar_tatuador, name="request_registrar_tatuador" ),

    # ---------- CERTIFICADO ---------- #
    path('certificacao/registrar/', registrar_certificado, name="registrar_certificado"),
    path('certificacao/editar/', editar_certificado, name="editar_certificado"),
    path('certificacao/remover/', remover_certificado, name="remover_certificado"),

    # ---------- BIOGRAFIA ---------- #
    path('bio/registrar/', registrar_bio, name="registrar_bio"),
    path('bio/editar/', editar_bio, name="editar_bio"),

    ##### ---------- API SERVICES ---------- #####

    path('api/v1/tatuadores/', tatuador_list),
    path('api/v1/tatuadores/nome/<str:nome>/', tatuador_list_by_name),
    path('api/v1/tatuadores/cidade/<str:cidade>/', tatuador_list_by_city),
]
