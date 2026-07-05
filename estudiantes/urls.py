from django.urls import path

from . import views

app_name = "estudiantes"

urlpatterns = [
    path("", views.EstudianteListView.as_view(), name="lista"),
    path("nuevo/", views.EstudianteCreateView.as_view(), name="crear"),
    path("<int:pk>/editar/", views.EstudianteUpdateView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.EstudianteDeleteView.as_view(), name="eliminar"),
]
