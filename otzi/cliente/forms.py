from django.core.mail.message import EmailMessage
from django.forms import ModelForm

class EmailForm(ModelForm):
    class Meta:
        #model = pass
        fields = ['__all__']

    def send_mail(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']

        conteudo = 'Nome do funcionario: %s \nE-mail de contato: %s'%(nome,email)

        mail = EmailMessage(
            subject = 'E-mail enviado pelo sistema projetoCurso',
            body = conteudo,
            from_email = 'gulissessti@hotmail.com',
            to = ['gulissessti@hotmail.com'],
            headers = {'Reply-To': email}
        )
        mail.send()
