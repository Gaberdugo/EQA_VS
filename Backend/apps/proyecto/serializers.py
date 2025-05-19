# apps/proyecto/serializers.py
from rest_framework import serializers
from .models import Ciudad, Departamento, Proyecto, ProyectoCiudad

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
    ciudades = serializers.SerializerMethodField(read_only=True)
    ciudades_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'ciudades', 'ciudades_ids']

    def get_ciudades(self, obj):
        return [{'id': ciudad.id, 'nombre': ciudad.nombre} for ciudad in obj.ciudades.all()]

    def create(self, validated_data):
        ciudades_ids = validated_data.pop('ciudades_ids', [])
        proyecto = Proyecto.objects.create(**validated_data)

        for ciudad_id in ciudades_ids:
            try:
                ciudad = Ciudad.objects.get(id=ciudad_id)
                ProyectoCiudad.objects.create(proyecto=proyecto, ciudades=ciudad)
            except Ciudad.DoesNotExist:
                raise serializers.ValidationError(f"Ciudad con id {ciudad_id} no existe.")

        return proyecto