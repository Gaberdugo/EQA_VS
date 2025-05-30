from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path("auth/", include('djoser.urls')),
    #path("auth/", include('djoser.urls.jwt')),
    path('auth/', include('apps.proyecto.urls')),
    path('auth/', include('apps.user.urls')),

    path('ins/', include('apps.institucion.urls')),

    path('res/', include('apps.respuestas.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]