from core.models import Abstract
from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
from stdimage import StdImageField
import uuid

from tatuador.models import Tatuador

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'usuario/foto_perfil/{uuid.uuid4()}.{ext}'
    return filename

class Usuario(Abstract):
    usuario = models.ForeignKey(User, verbose_name=("Usuario"), on_delete=models.CASCADE,null="True",blank=True)
    nome = models.CharField("Nome", max_length=300)
    desenhista = models.BooleanField('Desenhista', default=False)
    tatuador = models.OneToOneField(Tatuador,on_delete=models.SET_NULL, null=True, blank=True )
    imagem = StdImageField('Imagem', upload_to=get_file_path, 
        variations = {
            'thumbnail': (400, 400, True) ,
        }, null=True, blank=True
    )
    
    #def clean(self):
        #error_messages = {}
        #error_messages['username'] = 'O nome de usuário é obrigatório'
        #raise ValidationError(error_messages)
    
    def __str__(self):
        return f"{self.usuario}"

    class Meta:
        ordering = ['data_criacao']
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class PedidoOrcamento(Abstract):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario_solicitante")
    tatuadores = models.ManyToManyField(Tatuador, related_name="tatuadores")
    titulo = models.CharField('Titulo', max_length=255)
    texto_receptivo = models.CharField('Recepção', max_length=1000)
    parte_corpo = models.CharField('Parte do corpo', max_length=20)
    tamanho = models.CharField('Tamanho', max_length=40, help_text='Altura: 40cm x Largura: 20cm ')
    texto_complementar = models.TextField('Especificações e Descrição', max_length=2500)
    preco_esperado = models.DecimalField('Valor Esperado', max_digits=6, decimal_places=2)
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
    

# Create your models here.
