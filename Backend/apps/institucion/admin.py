# apps/proyecto/admin.py
from django.contrib import admin
from .models import Instituto

class InstitucionesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'municipio', 'departamento','DANE', 'terpel')
    search_fields = ('nombre', 'DANE',)

admin.site.register(Instituto, InstitucionesAdmin)