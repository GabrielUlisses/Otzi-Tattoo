# Generated by Django 3.0.3 on 2020-09-07 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tatuador', '0014_auto_20200831_2215'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bio',
            options={'ordering': ['data_criacao'], 'verbose_name': 'Biografia', 'verbose_name_plural': 'Biografias'},
        ),
        migrations.AlterField(
            model_name='bio',
            name='apresentacao',
            field=models.TextField(max_length=400, verbose_name='Apresentação'),
        ),
        migrations.AlterField(
            model_name='tatuador',
            name='bio',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tatuador.Bio'),
        ),
    ]
