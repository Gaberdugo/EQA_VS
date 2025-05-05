from rest_framework import serializers
from .models import Instituto

class InstitutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituto
        fields = ['id', 'nombre', 'municipio', 'DANE', 'terpel']  # Especificamos los campos que queremos incluir en el serializer
