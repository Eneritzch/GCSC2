from django.urls import path

from . import views

app_name = "cursos"

urlpatterns = [
    path("", views.CursoListView.as_view(), name="lista"),
    path("nuevo/", views.CursoCreateView.as_view(), name="crear"),
    path("<int:pk>/editar/", views.CursoUpdateView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.CursoDeleteView.as_view(), name="eliminar"),
]
