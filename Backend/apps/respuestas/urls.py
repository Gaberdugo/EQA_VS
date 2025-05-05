from django.urls import path
from .views import EncuestaView, EncuestaExportView, CuadernilloMateAPIView, EncuestaAleatoriaView, PreguntaView, CuadernillosNombresAPIView, EncuestaDeleteView, EncuestasResponsableView
from .views import ObtenerEncuestaAPIView, ModificarEncuestaAPIView, ObtenerInstitucionesAPIView,ObtenerMunicipiosAPIView,GenerarReporte1APIIew,GenerarReporte2APIIew, CrearInstitucionAPIView
 
urlpatterns = [
    path('respuesta/', EncuestaView.as_view(), name='repuesta_create'),  # Endpoint para crear la encuesta
    path('respuesta/exportar/', EncuestaExportView.as_view(), name='encuestas_export'),  # Endpoint para exportar encuestas a Excel
    path('instituciones/', ObtenerInstitucionesAPIView.as_view(), name='obtener_instituciones'),
    path('municipios/', ObtenerMunicipiosAPIView.as_view(), name='obtener_municipios'),
    path('pdf/', GenerarReporte1APIIew.as_view(), name='obtener_pdf'),
    path('pdf2/', GenerarReporte2APIIew.as_view(), name='obtener_pdf2'),
    path('cuadernillos/', CuadernilloMateAPIView.as_view(), name='cuadernillo_list'), 
    path('respuesta/aleatoria/', EncuestaAleatoriaView.as_view(), name='encuesta-aleatoria'),
    path("preguntas/", PreguntaView.as_view(), name="preguntas"),
    path('cuader/', CuadernillosNombresAPIView.as_view(), name='cuadernillos-nombres'),
    path('eliminar/', EncuestaDeleteView.as_view(), name='elimina-pregunta'),
    path('responsable/', EncuestasResponsableView.as_view(), name='responsable-preguntas'),
    path('obtener/<int:pk>/', ObtenerEncuestaAPIView.as_view(), name='obtener_encuesta'),
    path('modificar/', ModificarEncuestaAPIView.as_view(), name='modificar_encuesta'),
]
