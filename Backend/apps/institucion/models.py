from django.db import models

# Modelo institución
class Instituto(models.Model):
    nombre = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    departamento = models.CharField(max_length=255, default="")
    DANE = models.BigIntegerField(default=0) 
    terpel = models.IntegerField(default=0) 
