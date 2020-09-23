# Generated by Django 3.0.3 on 2020-03-30 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicacao', '0004_auto_20200329_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicacao',
            name='nr_aprovacoes',
            field=models.IntegerField(blank=True, null=True, verbose_name='Aprovações'),
        ),
        migrations.RemoveField(
            model_name='publicacao',
            name='aprovacoes',
        ),
        migrations.AddField(
            model_name='publicacao',
            name='aprovacoes',
            field=models.ManyToManyField(to='publicacao.Aprovacao'),
        ),
    ]
