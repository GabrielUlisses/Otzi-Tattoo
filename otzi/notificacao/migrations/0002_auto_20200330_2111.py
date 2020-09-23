# Generated by Django 3.0.3 on 2020-03-31 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notificacao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiponotificacao',
            name='cor',
            field=models.CharField(choices=[('muted', 'cinza claro'), ('primary', 'azul escuro'), ('success', 'verde claro'), ('info', 'azul claro'), ('warning', 'amarelo'), ('danger', 'vermelho'), ('secondary', 'cinza claro'), ('dark', 'preto'), ('body', 'escuro'), ('light', 'cinza bastante claro'), ('white', 'branco')], help_text='Cor usada na apresentação da Notificação', max_length=20, verbose_name='Cor'),
        ),
        migrations.AlterField(
            model_name='tiponotificacao',
            name='descricao',
            field=models.TextField(max_length=255, verbose_name='Descrição'),
        ),
    ]
