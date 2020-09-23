from django import forms
from django.core.validators import ValidationError
from django.forms.widgets import TextInput

from .models import *
from .plugins import cpf_validator

'''
class TatuadorEditForm(forms.ModelForm):
    class Meta:
        model = Tatuador
        fields = ["id","telefone","wathsapp","instagram","facebook","site_pessoal"]
        widgets = {
            'id': forms.HiddenInput(attrs={"id":"tatuador_id"}),
            'cpf': forms.TextInput(attrs={"class":"form-control","id":"cpf","placeholder":"000.000.000-00"}),
            'telefone': forms.TextInput(attrs={"class":"form-control","id":"telefone","placeholder":"(00) 0000-0000"}), 
            'wathsapp': forms.TextInput(attrs={"class":"form-control","id":"wathsapp",}), 
            'instagram': forms.TextInput(attrs={"class":"form-control","id":"instagram","placeholder":""}),
            'site_pessoal': forms.TextInput(attrs={"class":"form-control","id":"site_pessoal","placeholder":"seu site aqui"}),
        }

        help_texts = {
            'telefone': '(ddd) 0000-0000',
            'wathsapp': '(ddd) 0000-0000',
            'cpf': '123.123.123-12',
            'site_pessoal': 'www.meusite.com.br',
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf'].replace('.','').replace('-','')
        #if cpf_validator.cpf_validator(cpf) == "valido":
            #return self.cleaned_data['cpf']
        if cpf.isnumeric():
            return self.cleaned_data['cpf']
        else:
            raise ValidationError("Número de CPF inválido.")

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone'].replace('(','').replace(')','').replace('-','').replace(' ','')
        if  telefone.isnumeric():
            if  telefone.__len__() == 10 or  telefone.__len__() == 11:
                return self.cleaned_data['telefone']
            else:
                raise ValidationError("Tamanho Limite excedido.")
        else:
            raise ValidationError("Número de telefone inválido.")

    def clean_wathsapp(self):
        wathsapp = self.cleaned_data['wathsapp'].replace('(','').replace(')','').replace('-','').replace(' ','')
        if  wathsapp.isnumeric():
            if  wathsapp.__len__() == 10 or  wathsapp.__len__() == 11:
                return self.cleaned_data['wathsapp']
            else:
                raise ValidationError("Tamanho Limite excedido.")
        else:
            raise ValidationError("Número de wathsapp inválido.")
'''

class TatuadorForm(forms.ModelForm):
    
    class Meta:
        model = Tatuador
        exclude = ["bio","agenda","endereco", "ativo"]

        widgets = {
            'cpf': forms.TextInput(attrs={"class":"form-control","id":"cpf","placeholder":"000.000.000-00"}),
            'telefone': forms.TextInput(attrs={"class":"form-control","id":"telefone","placeholder":"(00) 0000-0000"}), 
            'wathsapp': forms.TextInput(attrs={"class":"form-control","id":"wathsapp",}), 
        }

        help_texts = {
            'telefone': '(ddd) 0000-0000',
            'wathsapp': '(ddd) 0000-0000',
            'cpf': '123.123.123-12',
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf'].replace('.','').replace('-','')
        #if cpf_validator.cpf_validator(cpf) == "valido":
            #return self.cleaned_data['cpf']
        if cpf.isnumeric():
            return self.cleaned_data['cpf']
        else:
            raise ValidationError("Número de CPF inválido.")

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone'].replace('(','').replace(')','').replace('-','').replace(' ','')
        if  telefone.isnumeric():
            if  telefone.__len__() == 10 or  telefone.__len__() == 11:
                return self.cleaned_data['telefone']
            else:
                raise ValidationError("Tamanho Limite excedido.")
        else:
            raise ValidationError("Número de telefone inválido.")

    def clean_wathsapp(self):
        wathsapp = self.cleaned_data['wathsapp'].replace('(','').replace(')','').replace('-','').replace(' ','')
        if  wathsapp.isnumeric():
            if  wathsapp.__len__() == 10 or  wathsapp.__len__() == 11:
                return self.cleaned_data['wathsapp']
            else:
                raise ValidationError("Tamanho Limite excedido.")
        else:
            raise ValidationError("Número de wathsapp inválido.")

class CertificacaoForm(forms.ModelForm):
    codigo = forms.CharField(initial="QRcode")
    class Meta:
        model = Certificacao
        fields = ['data','titulo','descricao','codigo','imagem']

        widgets = {
            'titulo': forms.TextInput(attrs={"class":"form-control","id":"titulo","placeholder":"Título aqui."}),
            'descricao': forms.Textarea(attrs={"class":"form-control","id":"descricao","placeholder":"Descrição aqui."}),
            'codigo': forms.TextInput(attrs={"class":"form-control","id":"codigo","placeholder":""}),
            #'data': forms.TextInput(attrs={"class":"form-control","id":"data","type":"date"})
            'data': forms.DateInput(attrs={"class":"form-control","id":"data","type":"date"})#,format="dd/mm/yyyy"
        }

        help_texts = {
            'titulo': "Título que consta no certificado",
            'descricao': "Descrição que consta no certificado",
            'data': "Data de emissão do certificado",
            'imagem': "Imagem digitalizada do certificado",
            'help_text':'Caso o mesmo seja em formato QRcode não altere o valor padrão "QRcode".'
        }

class CertificacaoEditForm(forms.ModelForm):
    codigo = forms.CharField(initial="QRcode")
    class Meta:
        model = Certificacao
        fields = ['data','titulo','descricao','codigo']

        widgets = {
            'titulo': forms.TextInput(attrs={"class":"form-control","id":"titulo","placeholder":"Título aqui."}),
            'descricao': forms.Textarea(attrs={"class":"form-control","id":"descricao","placeholder":"Descrição aqui."}),
            'codigo': forms.TextInput(attrs={"class":"form-control","id":"codigo","placeholder":""}),
            'data': forms.DateInput(attrs={"class":"form-control","id":"data",})#"type":"date"},format="dd/mm/yyyy"
        }

        help_texts = {
            'titulo': "Título que consta no certificado",
            'descricao': "Descrição que consta no certificado",
            'data': "Data de emissão do certificado",
            'imagem': "Imagem digitalizada do certificado",
            'help_text':'Caso o mesmo seja em formato QRcode não altere o valor padrão "QRcode".'
        }

class BioForm(forms.ModelForm):
    class Meta:
        model = Bio
        fields = ['apresentacao','conteudo']

        widgets = {
            'apresentacao': forms.TextInput(attrs={"class":"form-control","id":"apresentacao","placeholder":"Apresentação"}),
            'conteudo': forms.Textarea(attrs={"class":"form-control","id":"conteudo","placeholder":"Conteúdo da biografia...", 'rows':'5'}),
        }

        placeholder = {
            'apresentacao': "Texto apresentativo, não é obrigatório",
        }

        help_texts = {
            'apresentacao' : "Pequeno parágrafo de recepção para o leitor",
            'conteudo': "Espaço para o detalhamento da sua história como profissional amante das artes relacionadas a tatuagem"
        }