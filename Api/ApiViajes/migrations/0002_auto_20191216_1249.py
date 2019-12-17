# Generated by Django 2.1.13 on 2019-12-16 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ApiViajes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ext_pendienteenviar_costo',
            name='id',
        ),
        migrations.RemoveField(
            model_name='ext_pendienteenviar_precio',
            name='id',
        ),
        migrations.AlterField(
            model_name='ext_pendienteenviar_costo',
            name='IDPendienteEnviar',
            field=models.OneToOneField(db_column='IDPendienteEnviar', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ApiViajes.PendientesEnviar'),
        ),
        migrations.AlterField(
            model_name='ext_pendienteenviar_precio',
            name='IDPendienteEnviar',
            field=models.OneToOneField(db_column='IDPendienteEnviar', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ApiViajes.PendientesEnviar'),
        ),
    ]