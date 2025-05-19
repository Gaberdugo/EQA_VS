# apps/proyecto/serializers.py
from rest_framework import serializers
from .models import Ciudad, Departamento, Proyecto

class CiudadSerializer(serializers.ModelSerializer):
    departamento = serializers.PrimaryKeyRelatedField(queryset=Departamento.objects.all())
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)

    class Meta:
        model = Ciudad
        fields = ['id', 'nombre', 'departamento', 'departamento_nombre']


class DepartamentoSerializer(serializers.ModelSerializer):
    ciudades = CiudadSerializer(many=True, read_only=True)

    class Meta:
        model = Departamento
        fields = ['id','nombre', 'ciudades']

class ProyectoSerializer(serializers.ModelSerializer):
    ciudades = CiudadSerializer(many=True, read_only=True)

    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'ciudades']