from django.db import models

from stdimage import StdImageField

class Abstract(models.Model):
    data_criacao = models.DateTimeField('Data de Criação', auto_now=False, auto_now_add=True)
    ultima_modificacao = models.DateTimeField('Última Modificação', auto_now=True, auto_now_add=False)
    ativo = models.BooleanField('Ativo?', default=True)
    
    class Meta:
        abstract = True
    
