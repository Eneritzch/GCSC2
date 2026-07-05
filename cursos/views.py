from django.views.generic import ListView

from .models import Curso


class CursoListView(ListView):
    """Listado simple de cursos. Reutiliza la misma CBV genérica de Django."""

    model = Curso
    template_name = "cursos/curso_list.html"
    context_object_name = "cursos"
