from django.db import models
from core.models import Abstract
from stdimage import StdImageField
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'studio/foto_studio/{uuid.uuid4()}.{ext}'
    return filename

class Endereco(Abstract):
    UF = [
        ('AC','Acre'),
        ('AL','Alagoas'),
        ('AP','Amapá'),
        ('AM','Amazonas'),
        ('BA','Bahia'),
        ('CE','Ceará'),
        ('DF','Distrito Federal'),
        ('ES','ESpírito Santo'),
        ('GO','Goiás'),
        ('MA','Maranhão'),
        ('MT','Mato Grosso'),
        ('MS','Mato Grosso do Sul'),
        ('MG','Minas Gerais'),
        ('PA','Pará'),
        ('PB','Paraíba'),
        ('PR','Paraná'),
        ('PE','Pernanbuco'),
        ('PI','Piauí'),
        ('RJ','Rio de Janeiro'),
        ('RN','Rio Grande do Norte'),
        ('RS','Rio Grande do Sul'),
        ('RO','Rondônia'),
        ('RR','Roraima'),
        ('SC','Santa Catarina'),
        ('SP','São Paulo'),
        ('SE','Sergipe'),
        ('TO','Tocantins'),
    ]
    imagem = StdImageField('Imagem', upload_to=get_file_path, 
        variations = {
            'thumbnail': (400, 400, True) ,
        }, null=True, blank=True
    )
    cep = models.CharField('CEP', max_length=9)
    estado = models.CharField('Estado', max_length=2, choices=UF)
    cidade = models.CharField('Cidade', max_length=60)
    bairro = models.CharField('Bairro', max_length=60)
    rua = models.CharField('Rua', max_length=60)
    numero = models.CharField('N°', max_length=4)
    complemento = models.TextField('Complemento', max_length=100, null=True, blank=True, help_text="Informações adicionais sobre o endereço.")

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['cep']

    def __str__(self):
        return f'{self.cidade} / {self.estado}'

    def enderecos_por_estado(self):
        return Endereco.objects.filter(estado = self.estado)

    def enderecos_por_cidade(self):
        return Endereco.objects.filter(cidade = self.cidade)
