from django.db import models

from core.models import Abstract

DIA_SEMANA = [
    ('',''),
    ('segunda','Segunda'),
    ('terca','Terça'),
    ('quarta','Quarta'),
    ('quinta','Quinta'),
    ('sexta','Sexta'),
    ('sabado','Sábado'),
    ('domingo','Domingo'),
    ('feriado_religioso','Feriado Religioso'),
]

HORARIOS = [
    ('',''),
    ('nulo','Não informar.'),
    ('00:00','00:00'),
    ('01:00','01:00'),
    ('02:00','02:00'),
    ('03:00','03:00'),
    ('04:00','04:00'),
    ('05:00','05:00'),
    ('06:00','06:00'),
    ('07:00','07:00'),
    ('08:00','08:00'),
    ('09:00','09:00'),
    ('10:00','10:00'),
    ('11:00','11:00'),
    ('12:00','12:00'),
    ('13:00','13:00'),
    ('14:00','14:00'),
    ('15:00','15:00'),
    ('16:00','16:00'),
    ('17:00','17:00'),
    ('18:00','18:00'),
    ('19:00','19:00'),
    ('20:00','20:00'),
    ('21:00','21:00'),
    ('22:00','22:00'),
    ('23:00','23:00'),
]


class Agenda(Abstract):

    def __str__(self):
        return f'Agenda {self.tatuador}'

    class Meta:
        ordering = [ 'data_criacao']

class ConfiguracaoAgenda(Abstract):
    agenda = models.ForeignKey(Agenda, on_delete=models.PROTECT)
    dia = models.CharField('Dia', max_length=17, choices=DIA_SEMANA, default='')
    horario_inicio = models.CharField('Inicio de Expediente', max_length=5, choices=HORARIOS, default='08:00')
    horario_termino = models.CharField('Encerramento do Expediente', max_length=5 , choices=HORARIOS, default='18:00')
    horario_inicio_almoco = models.CharField('Pausa para o Almoço', max_length=5 , choices=HORARIOS, default='12:00', null = True, blank = True)
    horario_termino_almoco = models.CharField('Termino da Pausa do Almoço', max_length=5 , choices=HORARIOS, default='14:00', null = True, blank = True)

    def __str__(self):
        return f'{self.agenda} - {self.dia}'
    
    class Meta:
        verbose_name = 'Configuração de Agenda'
        verbose_name_plural = 'Configurações de Agenda'
        unique_together = ['agenda','dia']

