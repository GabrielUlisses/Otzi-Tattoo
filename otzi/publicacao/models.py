from django.db import models
from stdimage import StdImageField

from usuario.models import Usuario
from core.models import Abstract
from django.contrib.auth.models import User
from django.db.models import signals
import uuid

#TODO: Definir um slug_fy

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'usuario/foto_perfil/{uuid.uuid4()}.{ext}'
    return filename

class Publicacao(Abstract):
    publicante = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField('Título', max_length=255)
    conteudo = models.TextField('Conteúdo', max_length=2000, blank=True, null=True)
    midia = StdImageField(
        upload_to='usuario/publicacoes/',
        variations={
            'thumbnail':{'height':400, 'width':400, 'crop':True}
        },
        delete_orphans=True, 
        null=True,
        blank = True
    )
    nr_aprovacoes = models.IntegerField('Aprovações', null=True, blank=True)

    def __str__(self):
        return f'{self.titulo} - {self.publicante}'

    def aprovacoes(self):
        self.nr_aprovacoes = Aprovacao.objects.filter(publicacao = self).count()
        self.save()
        return self.nr_aprovacoes

        
    class Meta:
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'
        ordering = ['titulo', 'data_criacao']

class Aprovacao(Abstract):
    publicacao = models.ForeignKey(Publicacao, on_delete=models.PROTECT, default = 1)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, default = 1)

    def __str__(self):
        return f'{self.publicacao} - {self.usuario}'
    
    class Meta:
        verbose_name = 'Aprovação'
        verbose_name_plural = 'Aprovações'
        unique_together = ['publicacao', 'usuario']

# def produto_pre_save(signal,instance, sender, **kwargs):
#     instance.slug = slugify(instance.nome)

# signals.pre_save.connect(produto_pre_save, sender = Produto)