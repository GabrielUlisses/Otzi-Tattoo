from django import forms
from django.core.validators import ValidationError
from .models import *
   
class ConfiguracaoAgendaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoAgenda
        fields = ['dia','horario_inicio','horario_inicio_almoco','horario_termino_almoco','horario_termino']

    def clean_horario_inicio(self):
        #hi = int(self.data['horario_inicio'].replace(':',''))
        #ht = int(self.data['horario_termino'].replace(':',''))
        hi = self.data['horario_inicio']
        ht = self.data['horario_termino']
        if hi == 'nulo' or ht == 'nulo':
            raise ValidationError("Os horários de início e encerramento do expediente precisam ser informados.")
        else:
            hi = int(hi.replace(':', ''))
            ht = int(ht.replace(':', ''))
            if hi > ht:
                raise ValidationError("O Horário de início do expediente precisa ser menor que o horário de término.")
            elif hi == ht:
                raise ValidationError("Os horários de início e encerramento de expediente precisam ser diferentes.")
            else:
                return self.data['horario_inicio']    

    def clean_horario_termino(self):
        hi = self.data['horario_inicio']
        ht = self.data['horario_termino']
        if hi == 'nulo' or ht == 'nulo':
            raise ValidationError("Os horários de início e encerramento do expediente precisam ser informados.")
        else:
            hi = int(hi.replace(':', ''))
            ht = int(ht.replace(':', ''))
            if ht < hi:
                raise ValidationError("O Horário de início do expediente precisa ser menor que o horário de término.")
            elif hi == ht:
                raise ValidationError("Os horários de início e encerramento de expediente precisam ser diferentes.")
            else:
                return self.data['horario_termino']    

    def clean_horario_inicio_almoco(self):
        ia = self.data['horario_inicio_almoco']
        fa = self.data['horario_termino_almoco']
        hi = self.data['horario_inicio']
        ht = self.data['horario_termino']
        if ia == 'nulo' and fa == 'nulo':
            return self.data['horario_inicio_almoco']
        else:
            if (ia == 'nulo' and fa != 'nulo') or (ia != 'nulo' and fa == 'nulo'):
                raise ValidationError("Configuração inválida para o intervalo de almoço.")
            else: 
                ia = int(ia.replace(':',''))
                fa = int(fa.replace(':',''))
                if hi == 'nulo' or ht == 'nulo':
                    return None
                else:
                    hi = int(hi.replace(':', ''))
                    ht = int(ht.replace(':', ''))
        if ia > fa:
            raise ValidationError("O Horário de início do intervalo do almoço precisa ser menor que o horário de término.")
        elif ia == fa:
            raise ValidationError("Os horários de início e encerramento do intervalo de almoço precisam ser diferentes.")
        elif ia < hi or ia == hi:
            raise ValidationError("Configuração inválida")
        elif ia > ht or ia == ht:
            raise ValidationError("Configuração inválida")
        else:
            return self.data['horario_inicio_almoco']    

    def clean_horario_termino_almoco(self):
        ia = self.data['horario_inicio_almoco']
        fa = self.data['horario_termino_almoco']
        hi = self.data['horario_inicio']
        ht = self.data['horario_termino']
        if ia == 'nulo' and fa == 'nulo':
            return self.data['horario_termino_almoco']
        else:
            if (ia == 'nulo' and fa != 'nulo') or (ia != 'nulo' and fa == 'nulo'):
                raise ValidationError("Configuração inválida para o intervalo de almoço.")
            else: 
                ia = int(ia.replace(':',''))
                fa = int(fa.replace(':',''))
                if hi == 'nulo' or ht == 'nulo':
                    return None
                else:
                    hi = int(hi.replace(':', ''))
                    ht = int(ht.replace(':', ''))
        if fa < ia:
            raise ValidationError("O Horário de término do intervalo do almoço precisa ser maior que o horário de início.")
        elif ia == fa:
            raise ValidationError("Os horários de início e encerramento do intervalo de almoço precisam ser diferentes.")
        elif fa < hi or ia == hi:
            raise ValidationError("Configuração inválida")
        elif fa > ht or fa == ht:
            raise ValidationError("Configuração inválida")
        else:
            return self.data['horario_termino_almoco']    