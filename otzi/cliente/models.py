from django.db import models
from stdimage import StdImageField

from tatuador.models import Tatuador
from usuario.models import Usuario
from core.models import Abstract

"""
class PedidoOrcamento(Abstract):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False)
    tatuadores = models.ManyToManyField(Tatuador, limit_choices_to=6)
    titulo = models.CharField('Titulo', max_length=20)
    texto_receptivo = models.CharField('Recepção', max_length=100)
    parte_corpo = models.CharField('Parte do corpo', max_length=20)
    img_1 = StdImageField(
        upload_to = 'cliente/pedido_orcamento/',
        variations = {
            'thumbnail': {'width': 400, 'height': 400, 'crop': True}
        },
        delete_orphans = True,
        null = True, 
        blank = True
    )
    img_2 = StdImageField(
        upload_to = 'cliente/pedido_orcamento/',
        variations = {
            'thumbnail': {'width': 400, 'height': 400, 'crop': True}
        },
        delete_orphans=True,
        null = True, 
        blank = True
    )
    img_3 = StdImageField(
        upload_to = 'cliente/pedido_orcamento/',
        variations = {
            'thumbnail': {'width': 400, 'height': 400, 'crop': True}
        },
        delete_orphans=True,
        null = True, 
        blank = True
    )
    tamanho = models.CharField('Tamanho', max_length=40, help_text='Altura: 40cm x Largura: 20cm ')
    texto_complementar = models.TextField('Especificações e Descrição', max_length=300)
    preco_esperado = models.DecimalField('Valor esperado', max_digits=6, decimal_places=2)
"""