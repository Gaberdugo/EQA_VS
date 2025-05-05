from django.urls import path
from .views import CrearInstitucionAPIView, ObtenerDANEAPIView

urlpatterns = [
    path('institutos/', CrearInstitucionAPIView.as_view(), name='crear_instituto'),
    path('dane/', ObtenerDANEAPIView.as_view(), name='obtener_dane'),
]