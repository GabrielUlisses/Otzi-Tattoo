# Generated by Django 3.0.3 on 2020-06-14 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notificacao', '0011_auto_20200613_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificacao',
            name='visto',
        ),
    ]
