from .models import DenunciaPublicacao, DenunciaUsuario
from django import forms

class DenunciaPublicacaoForm(forms.ModelForm):
    class Meta:
        model = DenunciaPublicacao
        fields = ['tipo','descricao','publicacao','denunciante']
       
        widgets = {
            'descricao': forms.Textarea(attrs={'placeholder':'Área de descrição...','rows':'2'}),
            'publicacao': forms.Select(attrs={'style':'display:none;'}),
            'denunciante': forms.Select(attrs={'style':'display:none;'}),  
        }
            
        labels = {
            'descricao': "Detalhes e Observações",
            'publicacao': "",
            'denunciante': "",
            
        }

        help_text = {
            ''
            'tipo':'Selecione o tipo que melhor se enquadra com o ocorrido.',
            'descricao':'Quanto mais informações forem dadas à respeito do ocorrido mais simples se torna tomar as medidas cabíveis.'
        }

class DenunciaUsuarioForm(forms.ModelForm):
    class Meta:
        model = DenunciaUsuario
        exclude = ['ativo']

        widgets = {
            'denunciante': forms.TextInput(attrs={"style":"display: none;"}),
            'denunciado': forms.TextInput(attrs={"style":"display: none;"}),
            'descricao': forms.Textarea(attrs={"rows":"2"})
        }
        labels = {
            'descricao': "Detalhes e Observações",
            'denunciante': "",
            'denunciado': "",
        }
        help_text = {
            'tipo':'Selecione o tipo que melhor se enquadra com o ocorrido.',
            'descricao':'Quanto mais informações forem dadas à respeito do ocorrido mais simples se torna tomar as medidas cabíveis.',
            'imagem': 'Você pode enviar uma imagem que ajude a esclarecer o ocorrido.'
        }