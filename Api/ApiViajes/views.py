from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PendientesEnviar, RelacionConceptoxProyecto, Ext_PendienteEnviar_Costo, Ext_PendienteEnviar_Precio
from .serializers import PendientesEnviarSerializer
from django.db import transaction
import json

class PendientesEnviarList(APIView):

	#Trae todos los registros de la base de datos en la tabla PendientesEnviar
    def get(self, request):
        GetPendientesenviar = PendientesEnviar.objects.all()
        serializer = PendientesEnviarSerializer(GetPendientesenviar, many=True)
        return Response(serializer.data)

    #Crea el registro en la base de datos, en las tablas RelacionConceptoxProyecto, Ext_PendientEnviar_Costo (Proveedor), Ext_PrendienteEnviar_Precio (Cliente)
    # y el registro principal de PendientesEnviar
    def post(self, request):
        ArrConceptos = JSONParser().parse(request)
        #Verifica si se creara solamente 1 registro o se le paso un arreglo de viajes.
        if not isinstance(ArrConceptos, list):
            Aux = list()
            Aux.append(ArrConceptos)
            ArrConceptos = Aux
        transaction.set_autocommit(False)
        sid = transaction.savepoint()
        try:
            for data in ArrConceptos:
                serializer = PendientesEnviarSerializer(data=data)
                #Verifica que la informacion proporcionada coincida con la estructura de la tabla de PendientesEnviar, y verifica que por lo menos
                #se realizara factura para Cliente o Proveedor
                if serializer.is_valid() and (data["IsFacturaCliente"] or data["IsFacturaProveedor"]):
                    GetIDPendienteEnviar = serializer.save()
                    #Crea el registro de la tabla RelacionConceptoxProyecto
                    GetDataRelacionxProyecto = RelacionConceptoxProyecto(IDConcepto = data["IDConcepto"], IDPendienteEnviar_id= GetIDPendienteEnviar.IDPendienteEnviar, IDCliente= data["IDCliente"], IDProveedor= data["IDProveedor"])
                    GetDataRelacionxProyecto.save()
                    if data["IsFacturaCliente"]:
                    	#Crea el registro de la tabla Ext_PendienteEnviar_Precio para la informacion de cobro
                        if "MonedaPrecio" in data:
                            NewExtCliente = Ext_PendienteEnviar_Precio(IDPendienteEnviar=GetIDPendienteEnviar,
                                                                       PrecioSubtotal=data["PrecioSubtotal"],
                                                                       PrecioIVA=data["PrecioIVA"],
                                                                       PrecioRetencion=data["PrecioRetencion"],
                                                                       PrecioTotal=data["PrecioTotal"],
                                                                       MonedaPrecio=data["MonedaPrecio"])
                        else:
                            NewExtCliente = Ext_PendienteEnviar_Precio(IDPendienteEnviar=GetIDPendienteEnviar,
                                                                       PrecioSubtotal=data["PrecioSubtotal"],
                                                                       PrecioIVA=data["PrecioIVA"],
                                                                       PrecioRetencion=data["PrecioRetencion"],
                                                                       PrecioTotal=data["PrecioTotal"],
                                                                       MonedaPrecio=None)
                        if "ServiciosTotal" in data:
                            NewExtCliente.ServiciosIVA = data["ServiciosIVA"]
                            NewExtCliente.ServiciosRetencion = data["ServiciosRetencion"]
                            NewExtCliente.ServiciosSubtotal = data["ServiciosSubtotal"]
                            NewExtCliente.ServiciosTotal = data["ServiciosTotal"]
                        NewExtCliente.save()
                    if data["IsFacturaProveedor"]:
                    	#Crea el registro de la tabla Ext_PendienteEnviar_Costo para la informacion de Pago
                        if "MonedaCosto" in data:
                            NewExtProveedor = Ext_PendienteEnviar_Costo(IDPendienteEnviar=GetIDPendienteEnviar,
                                                                        CostoSubtotal=data["CostoSubtotal"],
                                                                        CostoIVA=data["CostoIVA"],
                                                                        CostoRetencion=data["CostoRetencion"],
                                                                        CostoTotal=data["CostoTotal"],
                                                                        MonedaCosto=data["MonedaCosto"])
                        else:
                            NewExtProveedor = Ext_PendienteEnviar_Costo(IDPendienteEnviar=GetIDPendienteEnviar,
                                                                        CostoSubtotal=data["CostoSubtotal"],
                                                                        CostoIVA=data["CostoIVA"],
                                                                        CostoRetencion=data["CostoRetencion"],
                                                                        CostoTotal=data["CostoTotal"],
                                                                        MonedaCosto=None)
                        NewExtProveedor.save()
                else:
                    raise Exception("Datos incorrectos")
        except Exception as e:
        	#Si hay algun error, se realiza un rollback para deshacer los cambios y se lanza un error 400
            transaction.savepoint_rollback(sid)
            transaction.set_autocommit(True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        transaction.commit()
        transaction.set_autocommit(True)
        return Response(GetIDPendienteEnviar.IDPendienteEnviar, status=status.HTTP_201_CREATED)

    #Se recibe un arreglo de folios para la eliminacion de estos en la base de datos
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
        	#Si hay algun error, se realiza un rollback para deshacer los cambios y se lanza un error 400
            transaction.savepoint_rollback(sid)
            transaction.set_autocommit(True)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        transaction.commit()
        transaction.set_autocommit(True)
        return Response(status=status.HTTP_200_OK)




class PendientesEnviarUpdate(APIView):
	#Trae la informacion del registro que coincide con el Folio proporcionado
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
        if "CostoIVA" in data:
            Ext_Costo = Ext_PendienteEnviar_Costo.objects.get(IDPendienteEnviar = Folio.IDPendienteEnviar)
            Ext_Costo.CostoIVA = data["CostoIVA"]
            Ext_Costo.CostoRetencion = data["CostoRetencion"]
            Ext_Costo.CostoSubtotal = data["CostoSubtotal"]
            Ext_Costo.CostoTotal = data["CostoTotal"]
            Ext_Costo.save()
        if "PrecioIVA" in data:
            Ext_Precio = Ext_PendienteEnviar_Precio.objects.get(IDPendienteEnviar = Folio.IDPendienteEnviar)
            Ext_Precio.PrecioIVA = data["PrecioIVA"]
            Ext_Precio.PrecioRetencion = data["PrecioRetencion"]
            Ext_Precio.PrecioSubtotal = data["PrecioSubtotal"]
            Ext_Precio.PrecioTotal = data["PrecioTotal"]
            if "ServiciosTotal" in data:
                Ext_Precio.ServiciosIVA = data["ServiciosIVA"]
                Ext_Precio.ServiciosRetencion = data["ServiciosRetencion"]
                Ext_Precio.ServiciosSubtotal = data["ServiciosSubtotal"]
                Ext_Precio.ServiciosTotal = data["ServiciosTotal"]
            Ext_Precio.save()
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Actualiza el registro del Folio especificado con la informacion que viene en un JSON. Los nombres de los parametros tienen que
    #corresponder a los nombres de cada campo en las tablas
    def patch(self, request, pk):
        try:
            Folio = PendientesEnviar.objects.get(Folio=pk)
        except PendientesEnviar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Se reemplaza la informacion de la tabla principal
        data = JSONParser().parse(request)
        serializer = PendientesEnviarSerializer(Folio, data=data, partial=True)
        #Se reemplaza la informacion de la tabla de costos, utilizada para el pago
        if "CostoIVA" in data:
            Ext_Costo = Ext_PendienteEnviar_Costo.objects.get(IDPendienteEnviar = Folio.IDPendienteEnviar)
            Ext_Costo.CostoIVA = data["CostoIVA"]
            Ext_Costo.CostoRetencion = data["CostoRetencion"]
            Ext_Costo.CostoSubtotal = data["CostoSubtotal"]
            Ext_Costo.CostoTotal = data["CostoTotal"]
            Ext_Costo.save()
        #Se reemplaza la informacion de la tabla de precios, utilizada para el cobro
        if "PrecioIVA" in data:
            Ext_Precio = Ext_PendienteEnviar_Precio.objects.get(IDPendienteEnviar = Folio.IDPendienteEnviar)
            Ext_Precio.PrecioIVA = data["PrecioIVA"]
            Ext_Precio.PrecioRetencion = data["PrecioRetencion"]
            Ext_Precio.PrecioSubtotal = data["PrecioSubtotal"]
            Ext_Precio.PrecioTotal = data["PrecioTotal"]
            if "ServiciosTotal" in data:
                Ext_Precio.ServiciosIVA = data["ServiciosIVA"]
                Ext_Precio.ServiciosRetencion = data["ServiciosRetencion"]
                Ext_Precio.ServiciosSubtotal = data["ServiciosSubtotal"]
                Ext_Precio.ServiciosTotal = data["ServiciosTotal"]
            Ext_Precio.save()
        if 'IDProveedor' in data:
            RelConceptoProveedor = RelacionConceptoxProyecto.objects.get(IDPendienteEnviar = Folio.IDPendienteEnviar)
            RelConceptoProveedor.IDProveedor = data["IDProveedor"]
            RelConceptoProveedor.save()
        if 'IDCliente' in data:
            RelConceptoCliente = RelacionConceptoxProyecto.objects.get(IDPendienteEnviar = Folio.IDPendienteEnviar)
            RelConceptoCliente.IDCliente = data["IDCliente"]
            RelConceptoCliente.save()
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Borra el registro del folio especificado en la URL
    def delete(self, request, pk):
        try:
            Folio = PendientesEnviar.objects.get(Folio=pk)
            Folio.delete()
            return Response(status=status.HTTP_200_OK)
        except PendientesEnviar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



#Esta funcion sirve para traer la informacion de las tablas de Costos y precios para poder regresarla en la consulta de los registros,
#de esta manera solo se tiene que consultar con 1 API para tener toda la infomacion.
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
