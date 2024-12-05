from rest_framework import serializers
from .models import Encuesta, PreguntaMate, CuadernilloMate, PreguntaLengua

class EncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta
        fields = '__all__'  # Incluye todos los campos del modelo Encuesta

class Encuesta2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta
        fields = [
            'id',
            'nombre'
            'nombre_estudiante',
            'fecha',
            'numero_cuadernillo',
            'respuesta_1',
            'respuesta_2',
            'respuesta_3',
            'respuesta_4',
            'respuesta_5',
            'respuesta_6',
            'respuesta_7',
            'respuesta_8',
            'respuesta_9',
            'respuesta_10',
            'respuesta_11',
            'respuesta_12',
            'respuesta_13',
            'respuesta_14',
            'respuesta_15',
            'respuesta_16',
            'respuesta_17',
            'respuesta_18',
            'respuesta_19',
            'respuesta_20',
        ]

class PreguntaMateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaMate
        fields = '__all__'  # Esto incluye todos los campos del modelo

# Serializador para los cuadernillos
class CuadernilloMateSerializer(serializers.ModelSerializer):
    # Incluimos las preguntas asociadas usando el PreguntaMateSerializer
    preguntas = PreguntaMateSerializer(many=True, read_only=True)

    class Meta:
        model = CuadernilloMate
        fields = '__all__'

class PreguntaLenguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaLengua
        fields = '__all__'  # Esto incluye todos los campos del modelo

class CuadernilloNombreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuadernilloMate  # Puedes usar este serializer para ambos modelos
        fields = ['nombre']
