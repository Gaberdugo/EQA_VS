from django.urls import path
from .views import EncuestaView, EncuestaExportView, CuadernilloMateAPIView, EncuestaAleatoriaView, PreguntaView, CuadernillosNombresAPIView, EncuestaDeleteView, EncuestasResponsableView

urlpatterns = [
    path('respuesta/', EncuestaView.as_view(), name='repuesta_create'),  # Endpoint para crear la encuesta
    path('respuesta/exportar/', EncuestaExportView.as_view(), name='encuestas_export'),  # Endpoint para exportar encuestas a Excel
    path('cuadernillos/', CuadernilloMateAPIView.as_view(), name='cuadernillo_list'), 
    path('respuesta/aleatoria/', EncuestaAleatoriaView.as_view(), name='encuesta-aleatoria'),
    path("preguntas/", PreguntaView.as_view(), name="preguntas"),
    path('cuader/', CuadernillosNombresAPIView.as_view(), name='cuadernillos-nombres'),
    path('eliminar/<int:pk>/', EncuestaDeleteView.as_view(), name='elimina-pregunta'),
    path('responsable/', EncuestasResponsableView.as_view(), name='responsable-preguntas')
]
