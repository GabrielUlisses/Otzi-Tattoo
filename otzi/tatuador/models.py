from django.db import models
from stdimage import StdImageField

from core.models import Abstract
from endereco.models import Endereco
from agenda.models import Agenda

# TODO: Definir método de get_file_instance para as imagens de upload e Definir métodos de busca personalizada

class Bio(Abstract):
    apresentacao = models.TextField('Apresentação', max_length=400)
    conteudo = models.TextField('Conteúdo', max_length=10000)

    def __str__(self):
        return f'Biografia - {self.apresentacao}'

    class Meta:
        verbose_name = 'Biografia'
        verbose_name_plural = 'Biografias'
        ordering = ['data_criacao']



class Tatuador(Abstract):
    bio = models.OneToOneField(Bio, on_delete=models.CASCADE, null=True, blank=True)
    cpf = models.CharField("CPF", max_length=14, unique=True, null=False, blank=False)
    telefone = models.CharField(max_length=16, unique=True, blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)
    agenda = models.OneToOneField(Agenda, on_delete=models.PROTECT, null=True)
    wathsapp = models.CharField("Wathsapp", max_length=20, null=True, blank=True)
    facebook = models.CharField("Facebook", max_length=255, null=True, blank=True)
    instagram = models.CharField("Instagram", max_length=255, null=True, blank=True)
    site_pessoal = models.CharField("Site Pessoal", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Tatuadores'
        verbose_name = 'Tatuador'

    def __str__(self):
        return f'Tatuador: {self.cpf}'

class Certificacao(Abstract):
    tatuador = models.ForeignKey(Tatuador, on_delete=models.CASCADE)
    data = models.DateField('Data da Certificação')
    titulo = models.CharField('Título', max_length=60)
    descricao = models.TextField('Descrição', max_length=500)
    codigo = models.CharField('Código de Validação', help_text='Caso o mesmo seja em formato QRcode não altere o valor padrão.', default='QR Code', max_length=20)
    imagem = StdImageField('Imagem',
        upload_to = 'tatuador/certificacao/',
        variations = {
            'thumbnail': { 'height': 400, 'width':400, 'crop': True}
        },
        delete_orphans=True,
        null = True,
        blank = True,
    )

    def __str__(self):
        return f'{self.titulo}'

    class Meta:
        verbose_name = 'Certificação'
        verbose_name_plural = 'Certificações'
        ordering = ['data_criacao', 'titulo']
        unique_together = ['tatuador','titulo']

