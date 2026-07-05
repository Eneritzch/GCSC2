from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("estudiantes/", include("estudiantes.urls")),
    path("reportes/", include("reportes.urls")),
    path("", RedirectView.as_view(pattern_name="estudiantes:lista", permanent=False)),
]
