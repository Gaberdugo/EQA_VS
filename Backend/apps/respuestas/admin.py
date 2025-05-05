from django.contrib import admin
from .models import Encuesta, PreguntaMate, CuadernilloMate, PreguntaLengua, CuadernilloLengua, Instituciones

class EncuestaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'ciudad', 'nombre_institucion', 'fecha', 'nombre_estudiante','grado', 'edad', 'genero', 'numero_cuadernillo', 'documento_estudiante', 'responsable', 'fecha_cargue']
    search_fields = ['nombre_estudiante', 'nombre_institucion', 'ciudad', 'aplicacion', 'prueba']
    list_filter = ['nombre', 'nombre_institucion', 'ciudad', 'edad', 'grado', 'numero_cuadernillo', 'responsable']

    # Personalización de campos, solo como ejemplo
    fields = ['nombre', 'ciudad', 'nombre_institucion', 'fecha', 'nombre_estudiante','grado', 'edad', 'genero', 'numero_cuadernillo', 'prueba', 'responsable', 'documento_estudiante']
    readonly_fields = ['fecha']

# Inline para mostrar las preguntas asociadas a un cuadernillo
class PreguntaMateInline(admin.TabularInline):
    model = CuadernilloMate.preguntas.through  # ManyToMany relationship table
    extra = 20  # Número de formularios vacíos adicionales que aparecerán

# Registrar el modelo CuadernilloMate en el admin
class CuadernilloMateAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Mostrar el nombre del cuadernillo en la lista
    search_fields = ('nombre',)  # Habilitar la búsqueda por nombre del cuadernillo
    inlines = [PreguntaMateInline]  # Mostrar las preguntas asociadas en línea en la vista de edición
    # Puedes añadir más personalización si lo necesitas

class PreguntaMateAdmin(admin.ModelAdmin):
    list_display = ('codigo_pregunta', 'grado', 'competencia', 'componente', 'dificultad', 'clave')
    search_fields = ('codigo_pregunta', 'competencia', 'componente')
    list_filter = ('grado', 'dificultad')
    ordering = ('grado',)

class PreguntaLenguaInline(admin.TabularInline):
    model = CuadernilloLengua.preguntas.through
    extra = 20

class CuadernilloLenguaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Mostrar el nombre del cuadernillo en la lista
    search_fields = ('nombre',)  # Habilitar la búsqueda por nombre del cuadernillo
    inlines = [PreguntaLenguaInline]  # Mostrar las preguntas asociadas en línea en la vista de edición
    # Puedes añadir más personalización si lo necesitas

class PreguntaLenguaAdmin(admin.ModelAdmin):
    list_display = ('codigo_pregunta', 'grado', 'competencia', 'dificultad', 'clave')
    search_fields = ('codigo_pregunta', 'competencia')
    list_filter = ('grado', 'dificultad')
    ordering = ('grado',)

class InstitucionesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'municipio','DANE', 'terpel')
    search_fields = ('nombre',)

admin.site.register(Encuesta, EncuestaAdmin)
admin.site.register(PreguntaMate, PreguntaMateAdmin) 
admin.site.register(CuadernilloMate, CuadernilloMateAdmin) 
admin.site.register(PreguntaLengua, PreguntaLenguaAdmin) 
admin.site.register(CuadernilloLengua, CuadernilloLenguaAdmin) 
admin.site.register(Instituciones, InstitucionesAdmin)
