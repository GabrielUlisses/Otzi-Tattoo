# Generated by Django 3.0.3 on 2020-04-07 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_auto_20200407_1413'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='configuracaoagenda',
            unique_together={('agenda', 'dia')},
        ),
    ]
