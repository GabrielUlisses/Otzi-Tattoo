# Generated by Django 3.0.3 on 2020-05-29 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_auto_20200423_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracaoagenda',
            name='dia',
            field=models.CharField(choices=[('', ''), ('segunda', 'Segunda'), ('terca', 'Terça'), ('quarta', 'Quarta'), ('quinta', 'Quinta'), ('sexta', 'Sexta'), ('sabado', 'Sábado'), ('domingo', 'Domingo'), ('feriado_religioso', 'Feriado Religioso')], default='', max_length=17, verbose_name='Dia'),
        ),
    ]
