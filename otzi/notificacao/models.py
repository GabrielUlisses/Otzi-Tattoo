from django.db import models
from core.models import Abstract
from usuario.models import Usuario
from django.contrib.auth.models import User


class TipoNotificacao(Abstract):
    COLOR = [
        ('muted','cinza claro'),
        ('primary','azul escuro'),
        ('success','verde claro'),
        ('info','azul claro'),
        ('warning','amarelo'),
        ('danger','vermelho'),
        ('secondary','cinza claro'),
        ('dark','preto'),
        ('body','escuro'),
        ('light','cinza bastante claro'),
        ('white','branco'),
    ]
    tipo = models.CharField('Tipo', max_length=20, help_text='Se refere ao tipo da notificação')
    cor = models.CharField('Cor', choices=COLOR, max_length=20,  help_text='Cor usada na apresentação da Notificação')
    descricao = models.TextField('Descrição', max_length=255,  help_text='')

    def __str__(self):
        return f'{self.tipo}'

    class Meta:
        verbose_name = 'Tipo de Notificação'
        verbose_name_plural = 'Tipos de Notificação'
        ordering = ['tipo']

class Notificacao(Abstract):
    titulo = models.CharField('Título', max_length=260)
    conteudo = models.TextField('Conteúdo', max_length=2000)
    emissor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emissor")
    destinatarios = models.ManyToManyField(User, through="NotificacaoUsuario")
    tipo = models.ForeignKey(TipoNotificacao, on_delete=models.CASCADE)
    #visto = models.BooleanField('Vizualizada', default="False", null=True, blank=True)

    def __str__(self):
        return f'{self.titulo} -  {self.tipo}'

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

class NotificacaoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    notificacao = models.ForeignKey(Notificacao, on_delete=models.CASCADE)
    recebido = models.BooleanField('Recebido', default=False)
    lido = models.BooleanField('Lido', default=False)

    def __str__(self):
        return f"{self.usuario} - {self.notificacao}"
