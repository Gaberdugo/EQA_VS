from django.urls import path
from .views import CrearInstitucionAPIView, ObtenerDANEAPIView, InstitucionesPorMunicipioAPIView, InstitucionesExcelAPIView
urlpatterns = [
    path('institutos/', CrearInstitucionAPIView.as_view(), name='crear_instituto'),
    path('dane/', ObtenerDANEAPIView.as_view(), name='obtener_dane'),
    path('municipio/', InstitucionesPorMunicipioAPIView.as_view(), name='instituciones_por_municipio'),
    path('instiexcel/', InstitucionesExcelAPIView.as_view(), name='excel_instituciones'),   
]