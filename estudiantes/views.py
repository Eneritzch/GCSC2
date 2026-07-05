from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import EstudianteForm
from .mixins import BusquedaMixin, FiltroCursoMixin
from .models import Estudiante


class EstudianteListView(BusquedaMixin, FiltroCursoMixin, ListView):
    """
    Lista paginada de estudiantes (10 por página).

    V2: se agregan BusquedaMixin (?q=) y FiltroCursoMixin (?curso_id=)
    reutilizando mixins genéricos; el cuerpo de la vista no cambia.
    """

    model = Estudiante
    template_name = "estudiantes/estudiante_list.html"
    context_object_name = "estudiantes"
    paginate_by = 10
    search_fields = ["nombre", "apellido", "email"]


class EstudianteCreateView(CreateView):
    """Alta de estudiante. Reutiliza EstudianteForm."""

    model = Estudiante
    form_class = EstudianteForm
    template_name = "estudiantes/estudiante_form.html"
    success_url = reverse_lazy("estudiantes:lista")


class EstudianteUpdateView(UpdateView):
    """Edición de estudiante. Reutiliza EL MISMO EstudianteForm que el alta."""

    model = Estudiante
    form_class = EstudianteForm
    template_name = "estudiantes/estudiante_form.html"
    success_url = reverse_lazy("estudiantes:lista")


class EstudianteDeleteView(DeleteView):
    """Baja de estudiante con confirmación."""

    model = Estudiante
    template_name = "estudiantes/estudiante_confirm_delete.html"
    success_url = reverse_lazy("estudiantes:lista")
