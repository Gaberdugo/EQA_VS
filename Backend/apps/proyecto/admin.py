# apps/proyecto/admin.py
from django.contrib import admin
from .models import Ciudad, Departamento, Proyecto, ProyectoCiudad

class ProyectoCiudadInline(admin.TabularInline):
    model = ProyectoCiudad
    extra = 1

# Personalizar el modelo
class ProyectoAdmin(admin.ModelAdmin):
    inlines = [ProyectoCiudadInline,]
    list_display = (
        'nombre',
    )

    filter_horizontal = ['ciudades',]

# Registrar los modelos en el panel de administración
admin.site.register(Departamento)
admin.site.register(Ciudad)
admin.site.register(Proyecto,ProyectoAdmin)