from django.db import models

# Create your models here.
class Transportistas(models.Model):
    IDTransportista = models.AutoField(primary_key=True)
    StatusProceso = models.CharField(max_length=50)
    class Meta:
        db_table="AdmonTransportistas"

class CartaNoAdeudoTransportistas(models.Model):
    IDCartaNoAdeudo = models.AutoField(primary_key=True)
    IDTransportista = models.ForeignKey(Transportistas, on_delete=models.CASCADE, db_column = 'IDTransportista')
    IDUsuarioAlta = models.IntegerField()
    IDUsuarioAprueba = models.IntegerField(default=None)
    IDUsuarioRechaza = models.IntegerField(default=None)
    FechaAlta = models.DateTimeField()
    MesCartaNoAdeudo = models.CharField(max_length=50)
    FechaAprueba = models.DateTimeField(default=None)
    FechaRechaza = models.DateTimeField(default=None)
    RutaCartaNoAdeudo = models.CharField(max_length=200)
    Status = models.CharField(max_length=100)
    ComentarioRechazo = models.CharField(max_length=300, default=None)
    Tipo = models.CharField(max_length=15)

    class Meta:
        db_table = "CartaNoAdeudoTransportistas"
        managed = False

class LogStatusTransportista(models.Model):
    IDLogStatusTransportista = models.AutoField(primary_key=True)
    IDTransportista = models.ForeignKey(Transportistas, on_delete=models.CASCADE, db_column="IDTransportista")
    IDUsuarioAlta = models.IntegerField()
    StatusAnterior = models.CharField(max_length=15)
    StatusActual = models.CharField(max_length=15)
    FechaCambio = models.DateTimeField()

    class Meta:
        db_table = "LogStatusTransportista"
        managed = False