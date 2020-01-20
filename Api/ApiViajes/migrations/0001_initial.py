# Generated by Django 2.1.13 on 2020-01-20 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PendientesEnviar',
            fields=[
                ('IDPendienteEnviar', models.AutoField(primary_key=True, serialize=False)),
                ('Folio', models.CharField(max_length=50, unique=True)),
                ('NombreCortoCliente', models.CharField(max_length=100)),
                ('NombreCortoProveedor', models.CharField(max_length=100)),
                ('FechaDescarga', models.DateTimeField()),
                ('Moneda', models.CharField(max_length=10)),
                ('Status', models.CharField(max_length=15)),
                ('IsEvidenciaFisica', models.BooleanField()),
                ('IsEvidenciaDigital', models.BooleanField()),
                ('Proyecto', models.CharField(max_length=30)),
                ('TipoConcepto', models.CharField(max_length=30)),
                ('IsControlDesk', models.BooleanField(default=False, null=True)),
            ],
            options={
                'db_table': 'PendientesEnviar',
            },
        ),
        migrations.CreateModel(
            name='RelacionConceptoxProyecto',
            fields=[
                ('IDRelacionConceptoxProyecto', models.AutoField(primary_key=True, serialize=False)),
                ('IDConcepto', models.IntegerField(default=0)),
                ('IDCliente', models.IntegerField(default=0)),
                ('IDProveedor', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'RelacionConceptoxProyecto',
            },
        ),
        migrations.CreateModel(
            name='Ext_PendienteEnviar_Costo',
            fields=[
                ('IDPendienteEnviar', models.OneToOneField(db_column='IDPendienteEnviar', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ApiViajes.PendientesEnviar')),
                ('CostoSubtotal', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('CostoIVA', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('CostoRetencion', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('CostoTotal', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('IsFacturaProveedor', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Ext_PendienteEnviar_Costo',
            },
        ),
        migrations.CreateModel(
            name='Ext_PendienteEnviar_Precio',
            fields=[
                ('IDPendienteEnviar', models.OneToOneField(db_column='IDPendienteEnviar', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ApiViajes.PendientesEnviar')),
                ('PrecioSubtotal', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('PrecioIVA', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('PrecioRetencion', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('PrecioTotal', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('PrecioServicios', models.DecimalField(decimal_places=5, default=0, max_digits=30)),
                ('IsFacturaCliente', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Ext_PendienteEnviar_Precio',
            },
        ),
        migrations.AddField(
            model_name='relacionconceptoxproyecto',
            name='IDPendienteEnviar',
            field=models.ForeignKey(db_column='IDPendienteEnviar', on_delete=django.db.models.deletion.CASCADE, to='ApiViajes.PendientesEnviar'),
        ),
    ]
