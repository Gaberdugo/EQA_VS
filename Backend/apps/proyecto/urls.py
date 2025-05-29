# apps/proyecto/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CiudadViewSet, DepartamentoViewSet, ProyectoViewSet, ProyectoExcelSet, ProyectoDetailView

# Creamos el router y registramos las vistas
router = DefaultRouter()
router.register(r'ciudades', CiudadViewSet, basename='ciudad')
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')

urlpatterns = [
    path('api/', include(router.urls)),  # Incluimos las URLs generadas por el router
    path('proyecto/', ProyectoViewSet.as_view(), name='proyecto'),
    path('proyecto/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto-detail'),
    path('excelPro/', ProyectoExcelSet.as_view(), name='Excel_proyecto')
]
