"""URLs raíz del proyecto control_estudiantes."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    # La app estudiantes es la página principal.
    path("estudiantes/", include("estudiantes.urls")),
    # Redirige la raíz a la lista de estudiantes.
    path("", RedirectView.as_view(pattern_name="estudiantes:lista", permanent=False)),
]
