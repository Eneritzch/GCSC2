from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from .views import git_history_view, git_history_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("historial/", git_history_view, name="historial"),
    path("api/git-graph/", git_history_api, name="git_graph_api"),
    path("estudiantes/", include("estudiantes.urls")),
    path("cursos/", include("cursos.urls")),
    path("reportes/", include("reportes.urls")),
    path("", RedirectView.as_view(pattern_name="estudiantes:lista", permanent=False)),
]
