from django.db import models

# Modelo Departamento
class Departamento(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

# Modelo Ciudad
class Ciudad(models.Model):
    nombre = models.CharField(max_length=255)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='ciudades')

    class Meta:
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return self.nombre

# Modelo Protyecto
class Proyecto(models.Model):
    nombre =  models.CharField(max_length=255, unique=True)
    ciudades = models.ManyToManyField(
        Ciudad,
        through='ProyectoCiudad',
        blank=True,
    )

    class Meta:
        pass

    def __str__(self):
        return self.nombre

class ProyectoCiudad(models.Model):
    ciudades = models.ForeignKey(Ciudad, on_delete=models.CASCADE, blank=True, null=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'proyecto_proyecto_ciudad'

    def __str__(self):
        return str(self.id) + '-' + self.proyecto.nombre