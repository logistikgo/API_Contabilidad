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
        try:
            Folio = PendientesEnviar.objects.get(Folio=pk)
            serializer = PendientesEnviarSerializer(Folio).data
            PendienteEnviar = PendienteEnviarToList(serializer)
            return Response(PendienteEnviar)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            Folio = PendientesEnviar.objects.get(Folio=pk)
        except PendientesEnviar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = JSONParser().parse(request)
        serializer = PendientesEnviarSerializer(Folio, data=data)
        if data["IsCosto"]:
            Ext_Costo = Ext_PendienteEnviar_Costo.objects.get(IDPendienteEnviar = Folio.IDPendienteEnviar)
            Ext_Costo.CostoIVA = data["CostoIVA"]
            Ext_Costo.CostoRetencion = data["CostoRetencion"]
            Ext_Costo.CostoSubtotal = data["CostoSubtotal"]
            Ext_Costo.CostoTotal = data["CostoTotal"]
            Ext_Costo.save()
        if data["IsPrecio"]:
            Ext_Precio = Ext_PendienteEnviar_Precio.objects.get(IDPendienteEnviar = Folio.IDPendienteEnviar)
            Ext_Precio.CostoIVA = data["PrecioIVA"]
            Ext_Precio.CostoRetencion = data["PrecioRetencion"]
            Ext_Precio.CostoSubtotal = data["PrecioSubtotal"]
            Ext_Precio.CostoTotal = data["PrecioTotal"]
            Ext_Precio.save()
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        Folio = PendientesEnviar.objects.get(Folio=pk)
        data = JSONParser().parse(request)
        serializer = PendientesEnviarSerializer(Folio, data=data, partial=True)
        if data["IsCosto"]:
            Ext_Costo = Ext_PendienteEnviar_Costo.objects.get(IDPendienteEnviar = Folio.IDPendienteEnviar)
            Ext_Costo.CostoIVA = data["CostoIVA"]
            Ext_Costo.CostoRetencion = data["CostoRetencion"]
            Ext_Costo.CostoSubtotal = data["CostoSubtotal"]
            Ext_Costo.CostoTotal = data["CostoTotal"]
            Ext_Costo.save()
        if data["IsPrecio"]:
            Ext_Precio = Ext_PendienteEnviar_Precio.objects.get(IDPendienteEnviar = Folio.IDPendienteEnviar)
            Ext_Precio.PrecioIVA = data["PrecioIVA"]
            Ext_Precio.PrecioRetencion = data["PrecioRetencion"]
            Ext_Precio.PrecioSubtotal = data["PrecioSubtotal"]
            Ext_Precio.PrecioTotal = data["PrecioTotal"]
            Ext_Precio.save()
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
            return Response(status=status.HTTP_404_NOT_FOUND)



def PendienteEnviarToList(PendienteMain):
    try:
        Ext_Costo = Ext_PendienteEnviar_Costo.objects.get(IDPendienteEnviar = PendienteMain["IDPendienteEnviar"])
        PendienteMain["CostoIVA"] = Ext_Costo.CostoIVA
        PendienteMain["CostoSubtotal"] = Ext_Costo.CostoSubtotal
        PendienteMain["CostoRetencion"] = Ext_Costo.CostoRetencion
        PendienteMain["CostoTotal"] = Ext_Costo.CostoTotal
    except Ext_PendienteEnviar_Costo.DoesNotExist:
        pass
    try:
        Ext_Precio = Ext_PendienteEnviar_Precio.objects.get(IDPendienteEnviar = PendienteMain["IDPendienteEnviar"])
        PendienteMain["PrecioIVA"] = Ext_Precio.PrecioIVA
        PendienteMain["PrecioSubtotal"] = Ext_Precio.PrecioSubtotal
        PendienteMain["PrecioRetencion"] = Ext_Precio.PrecioRetencion
        PendienteMain["PrecioTotal"] = Ext_Precio.PrecioTotal
    except Ext_PendienteEnviar_Precio.DoesNotExist:
        pass
    return PendienteMain