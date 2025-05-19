# apps/proyecto/views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Ciudad, Departamento, Proyecto
from .serializers import CiudadSerializer, DepartamentoSerializer, ProyectoSerializer

# Vista para el modelo Departamento
class DepartamentoViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

# Vista para el modelo Ciudad
class CiudadViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

class ProyectoViewSet(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Obtenemos todos los proyectos
        proyectos = Proyecto.objects.all()
        
        # Creamos el serializer con los proyectos
        serializer = ProyectoSerializer(proyectos, many=True)
        
        # Devolvemos la respuesta con los proyectos serializados
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProyectoSerializer(data=request.data)
        if serializer.is_valid():
            proyecto = serializer.save()
            return Response(ProyectoSerializer(proyecto).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
