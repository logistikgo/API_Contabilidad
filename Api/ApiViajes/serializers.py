from rest_framework import serializers
from .models import PendientesEnviar, RelacionConceptoxProyecto

class PendientesEnviarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendientesEnviar
        fields = '__all__'

class RelacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelacionConceptoxProyecto
        fields = ('RelacionIDConceptoxProyecto', 'IDConcepto', 'IDCliente', 'IDProveedor', 'Proyecto', 'IDPendienteEnviar')
