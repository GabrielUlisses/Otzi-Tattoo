# Generated by Django 3.0.3 on 2020-04-24 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tatuador', '0005_auto_20200417_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bio',
            name='tatuador',
        ),
        migrations.AddField(
            model_name='tatuador',
            name='bio',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='tatuador.Bio'),
        ),
    ]
