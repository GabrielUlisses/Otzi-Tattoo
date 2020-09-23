from .models import *
from django import forms

class PublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        fields = ['titulo','conteudo','midia','publicante']
        widgets = {
            'publicante': forms.HiddenInput(),
            'titulo': forms.TextInput(attrs={'class':"form-control",'max_length':'255','placeholder':'Título da publicação.'}),
            'conteudo': forms.Textarea(attrs={'class':'form-control', 'max_length':'2000', 'placeholder':'Conteúdo da publicação','rows':'3'}),
            'midia': forms.FileInput(attrs={ 'type':'file',"class":"custom-file-input" })
        }
        labels = {
            'titulo': 'Titulo',
            'conteudo': 'Conteúdo',
            'midia': 'Selecione uma imagem'
        }
        help_text = {
            'titulo': 'Insira o título da sua publicação',
            'conteudo': '',
            'midia': ''
        }
        error_messages = {
            'titulo': {},
            'conteudo': {},
            'midia': {},
        }
        
