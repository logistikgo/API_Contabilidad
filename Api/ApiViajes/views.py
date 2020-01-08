from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PendientesEnviar, RelacionConceptoxProyecto, Ext_PendienteEnviar_Costo, Ext_PendienteEnviar_Precio
from .serializers import PendientesEnviarSerializer
from django.db import transaction
import json

class PendientesEnviarList(APIView):

    def get(self, request):
        GetPendientesenviar = PendientesEnviar.objects.all()
        serializer = PendientesEnviarSerializer(GetPendientesenviar, many=True)
        return Response(serializer.data)

    def post(self, request):
        ArrConceptos = JSONParser().parse(request)
        if not isinstance(ArrConceptos, list):
            Aux = list()
            Aux.append(ArrConceptos)
            ArrConceptos = Aux
        transaction.set_autocommit(False)
        sid = transaction.savepoint()
        try:
            for data in ArrConceptos:
                serializer = PendientesEnviarSerializer(data=data)
                if serializer.is_valid() and (data["IsFacturaCliente"] or data["IsFacturaProveedor"]):
                    GetIDPendienteEnviar = serializer.save()
                    GetDataRelacionxProyecto = RelacionConceptoxProyecto(IDConcepto = data["IDConcepto"], IDPendienteEnviar_id= GetIDPendienteEnviar.IDPendienteEnviar, IDCliente= data["IDCliente"], IDProveedor= data["IDProveedor"])
                    GetDataRelacionxProyecto.save()
                    if data["IsFacturaCliente"]:
                        NewExtCliente = Ext_PendienteEnviar_Precio(IDPendienteEnviar = GetIDPendienteEnviar, PrecioSubtotal = data["PrecioSubtotal"], PrecioIVA = data["PrecioIVA"], PrecioRetencion = data["PrecioRetencion"], PrecioTotal = data["PrecioTotal"], PrecioServicios = data["PrecioServicios"])
                        NewExtCliente.save()
                    if data["IsFacturaProveedor"]:
                        NewExtProveedor = Ext_PendienteEnviar_Costo(IDPendienteEnviar = GetIDPendienteEnviar, CostoSubtotal = data["CostoSubtotal"], CostoIVA = data["CostoIVA"], CostoRetencion = data["CostoRetencion"], CostoTotal = data["CostoTotal"])
                        NewExtProveedor.save()
                else:
                    raise Exception("Datos incorrectos")
        except:
            transaction.savepoint_rollback(sid)
            transaction.set_autocommit(True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        transaction.commit()
        transaction.set_autocommit(True)
        return Response(GetIDPendienteEnviar.IDPendienteEnviar, status=status.HTTP_201_CREATED)

    def delete(self, request):
        ArrFolios = JSONParser().parse(request)
        if not isinstance(ArrFolios, list):
            Aux = list()
            Aux.append(ArrFolios)
            ArrFolios = Aux
        transaction.set_autocommit(False)
        sid = transaction.savepoint()
        try:
            for data in ArrFolios:
                Folio = PendientesEnviar.objects.get(Folio=data["Folio"])
                Folio.delete()
        except PendientesEnviar.DoesNotExist:
            pass
        except:
            transaction.savepoint_rollback(sid)
            transaction.set_autocommit(True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        transaction.commit()
        transaction.set_autocommit(True)
        return Response(status=status.HTTP_200_OK)




class PendientesEnviarUpdate(APIView):
    def get(self, request, pk):
        Folio = PendientesEnviar.objects.get(Folio=pk)
        serializer = PendientesEnviarSerializer(Folio)
        return Response(serializer.data)

    def put(self, request, pk):
        Folio = PendientesEnviar.objects.get(Folio=pk)
        data = JSONParser().parse(request)
        serializer = PendientesEnviarSerializer(Folio, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        Folio = PendientesEnviar.objects.get(Folio=pk)
        data = JSONParser().parse(request)
        serializer = PendientesEnviarSerializer(Folio, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Folio = PendientesEnviar.objects.get(Folio=pk)
        if Folio:
            Folio.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_not_found)
