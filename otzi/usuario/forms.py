from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.validators import EmailValidator, validate_email
from rest_framework.fields import CharField

#from .plugins import cpf_validator
from .models import *


class UserForm(ModelForm):
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={ "class":"form-control"}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))

    def clean_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.data['confirm_password']
        if password != confirm_password:
            raise ValidationError("As senhas precisam ser iguais")
        else:
            return password

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            email = validate_email(email)
        except:
            raise ValidationError("Insira um e-mail válido.")
        return email

    class Meta:
        model = User
        fields = ('username','password','confirm_password','email')

        widgets = {
            'username': forms.TextInput(attrs={"class":"form-control"}),
            'email': forms.TextInput(attrs={"class":"form-control"})
        }
        labels = {
            'username' : ('Login'),
            'password' : ('*******'),
            'email': ('E-mail'),
            'confirm_senha': ('*******'),
        }
        help_texts = {
            'username': (''),
            'password': (''),
            'email': ('exemploDeEmail@e-mail.com'),
            'confirm_senha': (''),
        }
        error_messages = {
            'username': {
                'max_length': ('O número de caracteres inseridos excede o limite estabelecido.'),
            },
            'password': {
                'max_length': ('O número de caracteres inseridos excede o limite estabelecido.'),
                'validate_email': ('Insira um e-mail válido.')
            },
            'confirm_password': {
                'max_length': ('O número de caracteres inseridos excede o limite estabelecido.'),
            },
            'email': {
                'max_length': ('O número de caracteres inseridos excede o limite estabelecido.'),
            },
        }

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    labels = {
        'username' : ('Login'),
        'email': ('E-mail'),           
    },
    help_texts = {
        'username': (''),
        'email': ('email@example.com'),
    }
    error_messages = {
        'username': {
            'max_length': ('O número de caracteres inseridos excede o limite estabelecido.'),
        },
        'email': {
            'max_length': ('O número de caracteres inseridos excede o limite estabelecido.'),
        },
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            em = validate_email(email)
        except:
            raise ValidationError("Insira um e-mail válido.")
        return email

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ("nome",'imagem',"desenhista",) 

        widgets = {
            "nome": forms.TextInput(attrs={"class":"form-control"}),
            "imagem": forms.FileInput(attrs={"class":"custom-file-input"}),
            "desenhista": forms.CheckboxInput(attrs={"class":"custom-control-input"})
        }   

        labels = {
            'imagem' : ('Escolha uma foto de perfil'),
            'desenhista': ('Deseja possuir o perfil de desenhista?'),
            'nome': ('Nome Completo'),
        }
        help_texts = {
            'imagem': (""),
            'desenhista': ("Deseja especializar seu perfil para desenhista ?"),
            'nome': ("Seu nome completo"),
        }
        error_messages = {
            'imagem': {
            },
            'desenhista': {
            },
        }

class PedidoOrcamentoForm(ModelForm):
    usuario_id = forms.CharField(max_length=8, widget=forms.HiddenInput(attrs={"id":"usuario_id","name":"usuario_id"}))   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['titulo'].initial = "Pedido de Orçamento"
        self.fields['texto_receptivo'].initial = "Olá, gostaria de me informar sobre um valor aproximado de uma tatuagem de acordo com as informações a seguir"
        #self.fields['texto_complementar'].initial = "Especificações, técnicas ou efeitos desejáveis, dentre outras informações que facilitem a compreensão da arte desejada."

    class Meta:
        model = PedidoOrcamento
        exclude = ["ativo","tatuadores"]

        widgets = {        
            'texto_complementar': forms.Textarea(attrs={"rows":"2"}) ,       
            'texto_receptivo': forms.Textarea(attrs={"rows":"2"}),  
            'usuario': forms.HiddenInput(attrs={"id":"usuario","name":"usuario"}) 
            #'img_1': forms.FileInput(attrs={"class":"custom-file-input"}),  
        }
        help_texts = {
            'preco_esperado': "EX: R$ 400,00",
            'parte_corpo': "Exemplos: Costas, Braço, Do ombro ao antebraço "
        }
        labels = {
            'img_1': "1° Imagem",
            'img_2': "2° Imagem",
            'img_3': "3° Imagem",
        },
        place_holder = {
            'texto_complementar': "Especificações, técnicas ou efeitos desejáveis, dentre outras informações que facilitem a compreensão da arte desejada."
        }
        error_messages = {}

    def clean_usuario_id(self):
        usuario_id = self.cleaned_data["usuario_id"]   
        if not str(usuario_id).isnumeric():
            raise ValidationError("O id recebido é não numérico")
        return usuario_id
