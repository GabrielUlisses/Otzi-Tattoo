# Generated by Django 3.0.3 on 2020-03-30 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_auto_20200324_0933'),
        ('publicacao', '0002_auto_20200324_0933'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='aprovacao',
            unique_together={('publicacao', 'usuario')},
        ),
    ]
