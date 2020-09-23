from django.db import models
from stdimage import StdImageField

from core.models import Abstract
from usuario.models import User
from publicacao.models import Publicacao

#TODO: Avaliar a elaboração de métodos para listagem de dados filtrada

class TipoDenuncia(Abstract):
    tipo = models.CharField('Tipo', max_length=20, help_text='')
    descricao = models.TextField('Descrição', max_length=200)
    aviso = models.CharField('Implicações', max_length=60, help_text='Descreva as implicações ao se usar esse tipo de denúncia', default="Nenhuma")

    def __str__(self):
        return f'{self.tipo}'

    class Meta:
        verbose_name = 'Tipo de Denúncia'
        verbose_name_plural = 'Tipos de Denúncia'
        ordering = ['tipo']

class Denuncia(Abstract):
    denunciante = models.ForeignKey(User, on_delete=models.PROTECT)
    descricao = models.TextField('Descrição', max_length=2000, null=True, blank=True)
    tipo = models.ForeignKey(TipoDenuncia, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        verbose_name = 'Denúncia'
        verbose_name_plural = 'Denúncias'
        ordering = ['data_criacao', 'ativo']

class DenunciaUsuario(Denuncia):
    denunciado = models.ForeignKey(User, related_name="denuncia_usuario_denunciado",on_delete=models.PROTECT, null=True)
    imagem = StdImageField(
        upload_to ='usuario/denuncia/',
        variations = {
            'thumbnail': {'height': 400, 'width': 400, 'crop': True}
        },
        delete_orphans=True,
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.denunciado} - {self.tipo}'

    class Meta:
        ordering = ['data_criacao']
        verbose_name = 'Denúncia contra Usuário'
        verbose_name = 'Denúncia contra Usuários'

class DenunciaPublicacao(Denuncia):
    publicacao = models.ForeignKey(Publicacao, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.publicacao} - {self.tipo}'

    class Meta:
        ordering = ['data_criacao']
        verbose_name = 'Denúncia contra Publicação'
        verbose_name_plural = 'Denúncia contra Publicações'