from django.db import models
from django.contrib.auth.models import User

from usuario.models import Usuario

from notificacao.views import gerar_notificacao
from notificacao.models import Notificacao, NotificacaoUsuario, TipoNotificacao

class Message(models.Model):
    author = models.ForeignKey(User, related_name="author_message", on_delete=models.CASCADE)
    to = models.ForeignKey(User, related_name="user_message", on_delete=models.CASCADE)
    message = models.CharField("Content Message", max_length=1000)
    time = models.DateTimeField("TimeStamp", auto_now_add=True)

    class Meta:
        #db_table = "chat_message"
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"


def get_last_messages(user, to):
    msg1 = Message.objects.filter(author=user, to=to)
    msg2 = Message.objects.filter(author=to, to=user)
    return msg1.union(msg2).order_by("time")


def not_routine(user_emiss, user_dest, url):
    tipo = TipoNotificacao.objects.get(tipo="Comum")

    user = User.objects.get(username=user_emiss)
    to = User.objects.get(username=user_dest)

    n = Notificacao.objects.filter(emissor__username=user, destinatarios__username=to.username,  tipo=tipo).last()
    if n:
        n_u = NotificacaoUsuario.objects.get(notificacao = n)
        if n_u.lido == True:
            gerar_notificacao(
                to,
                titulo = "Você recebeu novas mensagens",
                emissor = user,
                conteudo = f" O usuário {user} lhe enviou novas mensagens <a href='http://{url}' class='text-info' >veja o chat</a>",
                tipo = tipo
            )
    else:
        gerar_notificacao(
                to,
                titulo = "Você recebeu novas mensagens",
                emissor = user,
                conteudo = f" O usuário {user} lhe enviou novas mensagens <a href='http://{url}' class='text-info' >veja o chat</a>",
                tipo = tipo
            )

"""
class Chat(models.Model):
    users = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message)
    """