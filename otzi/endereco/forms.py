from django.forms import ModelForm
from django import forms
from .models import Endereco

class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep','cidade','bairro','estado','rua','numero','complemento']

        widgets = {
            'cep': forms.TextInput(attrs={"class":"form-control cep-mask","placeholder":"00000-000","id":"cep"}),
            'cidade': forms.TextInput(attrs={"class":"form-control texto","id":"cidade","style":"text-transform: uppercase;"}),
            'bairro': forms.TextInput(attrs={"class":"form-control texto","id":"bairro","style":"text-transform: uppercase;"}),
            'estado': forms.Select(attrs={"class":"form-control","id":"estado"}),
            'rua': forms.TextInput(attrs={"class":"form-control texto","id":"rua","style":"text-transform: uppercase;"}),
            'numero': forms.TextInput(attrs={"class":"form-control","id":"numero"}),
            'complemento': forms.Textarea(attrs={"class":"form-control texto","id":"complemento","rows":"3","style":"text-transform: uppercase;"}),
        }
        help_texts = {
            'cep': ('ex. 85875-000'),
            'rua': ('Av. Almeida Freitas, rua. Paraiba'),
            'numero': ('ex. n°1234')
        }
        labels = {
            
        }
    def clean_numero(self):
        num = self.cleaned_data['numero']
        if num.__len__() > 4:
            raise forms.ValidationError("Número residencial inválido.")
        elif not num.isnumeric():
            raise forms.ValidationError("Apenas números são permitidos.")
        else:
            return num
       