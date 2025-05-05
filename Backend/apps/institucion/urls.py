from django.urls import path
from .views import CrearInstitucionAPIView

urlpatterns = [
    path('institutos/', CrearInstitucionAPIView.as_view(), name='crear_instituto'),
]