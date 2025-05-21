from rest_framework import permissions
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Instituto
from .serializers import InstitutoSerializer, InstitutoNombreSerializer
from rest_framework.permissions import AllowAny

import pandas as pd

class CrearInstitucionAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = InstitutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtenerDANEAPIView(APIView):
    def get(self, request):
        nombre = request.GET.get('nombre')

        if not nombre:
            return Response({"error": "El parámetro 'nombre' es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        institucion = Instituto.objects.filter(nombre=nombre).first()

        if institucion:
            return Response({"DANE": institucion.DANE}, status=status.HTTP_200_OK)
        else:
            return Response({"DANE": 9999}, status=status.HTTP_200_OK)

class InstitucionesPorMunicipioAPIView(APIView):
    def get(self, request):
        municipio = request.GET.get('municipio')

        if not municipio:
            return Response({"error": "El parámetro 'municipio' es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        instituciones = Instituto.objects.filter(municipio=municipio)
        serializer = InstitutoNombreSerializer(instituciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InstitucionesExcelAPIView(APIView):
    def get(self, request):
        
        instituciones = Instituto.objects.all()

        # Si no hay encuestas para el proyecto proporcionado
        if not instituciones:
            return Response({"error": "No se encontraron encuestas para el proyecto proporcionado."}, status=404)
        
        data = []
        for instituto in instituciones:
            try:
                data.append({
                        'Instituto' : instituto.nombre,
                        'Municipio' : instituto.municipio,
                        'Departamento' : instituto.departamento,
                        'DANE' : instituto.DANE
                })
            except :
                pass

        # Crear un DataFrame de pandas con los datos
        df = pd.DataFrame(data)

        # Crear la respuesta HTTP para descargar el archivo Excel
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=institutos.xlsx'

        # Escribir el DataFrame a un archivo Excel en la respuesta
        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

        return response
