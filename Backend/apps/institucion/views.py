from rest_framework import permissions
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Instituto
from .serializers import InstitutoSerializer
from rest_framework.permissions import AllowAny

def valorDane(nombre):
    institucion = Instituto.objects.filter(nombre=nombre)
    if institucion.exists():
        res = int(institucion.DANE)
    else:
        res = 9999
    
    return res

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
