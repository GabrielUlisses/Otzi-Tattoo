# Generated by Django 3.0.3 on 2020-06-15 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notificacao', '0012_remove_notificacao_visto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacao',
            name='conteudo',
            field=models.TextField(max_length=2000, verbose_name='Conteúdo'),
        ),
        migrations.AlterField(
            model_name='notificacao',
            name='titulo',
            field=models.CharField(max_length=260, verbose_name='Título'),
        ),
    ]
