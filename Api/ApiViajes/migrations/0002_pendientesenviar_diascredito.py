# Generated by Django 2.1.13 on 2020-01-21 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiViajes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendientesenviar',
            name='DiasCredito',
            field=models.IntegerField(default=30),
        ),
    ]
