# apps/proyecto/views.py
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Ciudad, Departamento, Proyecto
from .serializers import CiudadSerializer, DepartamentoSerializer, ProyectoSerializer

import pandas as pd

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
    
class ProyectoDetailView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        try:
            proyecto = Proyecto.objects.get(pk=pk)
            proyecto.delete()
            return Response({"message": "✅ Proyecto eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except Proyecto.DoesNotExist:
            return Response({"error": "❌ Proyecto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
class ProyectoExcelSet(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Obtenemos todos los proyectos
        proyectos = Proyecto.objects.all()

        data = []

        for proyecto in proyectos:
            for ciudad in proyecto.ciudades.all():
                try:
                    data.append({
                            'ID Proyecto' : proyecto.id,
                            'Proyecto' : proyecto.nombre,
                            'Municipio' : ciudad.nombre,
                            'Departamento': ciudad.departamento.nombre if ciudad.departamento else ''
                    })
                except :
                    pass


        # Crear un DataFrame de pandas con los datos
        df = pd.DataFrame(data)

        # Crear la respuesta HTTP para descargar el archivo Excel
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=proyectos.xlsx'

        # Escribir el DataFrame a un archivo Excel en la respuesta
        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

        return response
