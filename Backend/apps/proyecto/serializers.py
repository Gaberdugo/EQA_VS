# apps/proyecto/serializers.py
from rest_framework import serializers
from .models import Ciudad, Departamento, Proyecto

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['nombre']

class CiudadSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer(read_only=True) 

    class Meta:
        model = Ciudad
        fields = ['nombre', 'departamento']

class ProyectoSerializer(serializers.ModelSerializer):
    ciudades = CiudadSerializer(many=True, read_only=True)

    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'ciudades']