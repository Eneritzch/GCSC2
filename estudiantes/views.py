from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import EstudianteForm
from .models import Estudiante


class EstudianteListView(ListView):
    model = Estudiante
    template_name = "estudiantes/estudiante_list.html"
    context_object_name = "estudiantes"
    paginate_by = 10


class EstudianteCreateView(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "estudiantes/estudiante_form.html"
    success_url = reverse_lazy("estudiantes:lista")


class EstudianteUpdateView(UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "estudiantes/estudiante_form.html"
    success_url = reverse_lazy("estudiantes:lista")


class EstudianteDeleteView(DeleteView):
    model = Estudiante
    template_name = "estudiantes/estudiante_confirm_delete.html"
    success_url = reverse_lazy("estudiantes:lista")
