# Generated by Django 3.0.3 on 2020-04-23 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tatuador', '0005_auto_20200417_1753'),
        ('agenda', '0004_auto_20200422_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='tatuador',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='tatuador.Tatuador'),
        ),
    ]
