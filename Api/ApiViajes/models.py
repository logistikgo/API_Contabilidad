from django.db import models

class PendientesEnviar(models.Model):
    IDPendienteEnviar = models.AutoField(primary_key=True)
    Folio = models.CharField(max_length=50, unique=True)
    NombreCortoCliente = models.CharField(max_length=100)
    NombreCortoProveedor = models.CharField(max_length=100)
    FechaDescarga = models.DateTimeField()
    Moneda = models.CharField(max_length=10)
    Status = models.CharField(max_length=15)
    IsEvidenciaFisica = models.BooleanField()
    IsEvidenciaDigital = models.BooleanField()
    Proyecto = models.CharField(max_length=30)
    TipoConcepto = models.CharField(max_length=30)
    class Meta:
        db_table="PendientesEnviar"


class Ext_PendienteEnviar_Costo(models.Model):
    IDPendienteEnviar = models.OneToOneField(PendientesEnviar, on_delete=models.CASCADE, db_column = 'IDPendienteEnviar', primary_key=True)
    CostoSubtotal = models.DecimalField(default=0, max_digits=30, decimal_places=5)
    CostoIVA = models.DecimalField(default=0, max_digits=30, decimal_places=5)
    CostoRetencion = models.DecimalField(default=0, max_digits=30, decimal_places=5)
    CostoTotal = models.DecimalField(default=0, max_digits=30, decimal_places=5)
    IsFacturaProveedor = models.BooleanField(default=False)
    class Meta:
        db_table="Ext_PendienteEnviar_Costo"


class Ext_PendienteEnviar_Precio(models.Model):
    IDPendienteEnviar = models.OneToOneField(PendientesEnviar, on_delete=models.CASCADE, db_column = 'IDPendienteEnviar', primary_key=True)
    PrecioSubtotal = models.DecimalField(default=0, max_digits=30, decimal_places=5)
    PrecioIVA = models.DecimalField(default=0, max_digits=30, decimal_places=5)
    PrecioRetencion = models.DecimalField(default=0, max_digits=30, decimal_places=5)
    PrecioTotal = models.DecimalField(default=0, max_digits=30, decimal_places=5)
    PrecioServicios = models.DecimalField(default=0, max_digits=30, decimal_places=5)
    IsFacturaCliente = models.BooleanField(default=False)
    class Meta:
        db_table="Ext_PendienteEnviar_Precio"


class RelacionConceptoxProyecto(models.Model):
    IDRelacionConceptoxProyecto = models.AutoField(primary_key=True)
    IDPendienteEnviar = models.ForeignKey(PendientesEnviar, on_delete=models.CASCADE, db_column = 'IDPendienteEnviar')
    IDConcepto = models.IntegerField(default=0)
    IDCliente = models.IntegerField(default=0)
    IDProveedor = models.IntegerField(default=0)
    class Meta:
        db_table="RelacionConceptoxProyecto"