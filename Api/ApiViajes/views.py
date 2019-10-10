from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PendientesEnviar, RelacionConceptoxProyecto
from .serializers import PendientesEnviarSerializer

class PendientesEnviarList(APIView):

    def get(self, request):
        GetPendientesenviar = PendientesEnviar.objects.all()
        serializer = PendientesEnviarSerializer(GetPendientesenviar, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PendientesEnviarSerializer(data=data)
        if serializer.is_valid():
            GetIDPendienteEnviar = serializer.save()
            GetDataRelacionxProyecto = RelacionConceptoxProyecto(IDConcepto= data["IDConcepto"], IDPendienteEnviar_id= GetIDPendienteEnviar.IDPendienteEnviar, IDCliente= data["IDCliente"], IDProveedor= data["IDProveedor"], Proyecto= data["Proyecto"])
            GetDataRelacionxProyecto.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)




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

