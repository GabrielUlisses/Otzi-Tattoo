from os.path import defpath

from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'enderecos', EnderecoViewSet)


urlpatterns = [
    path('api/v1/',include(router.urls)),
    path('studio/editar/', editar_dados_studio, name="editar_dados_studio"),

    path('api/v1/studio/', StudioApiView.as_view(), name="get_studios"),
    path('api/v1/studio/<str:param>/', StudioApiView.as_view(), name="get_studios"),
]
