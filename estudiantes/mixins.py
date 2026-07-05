"""Mixins reutilizables para las vistas de la app estudiantes."""

from django.db.models import Q


class BusquedaMixin:
    """Agrega busqueda por texto (?q=) a cualquier ListView via search_fields."""

    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(q_objects)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class FiltroCursoMixin:
    """Agrega filtro por curso (?curso_id=) a cualquier ListView."""

    curso_field = "curso_id"

    def get_queryset(self):
        queryset = super().get_queryset()
        curso_id = self.request.GET.get("curso_id")
        if curso_id:
            queryset = queryset.filter(**{self.curso_field: curso_id})
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from cursos.models import Curso

        context["cursos"] = Curso.objects.all()
        context["curso_id"] = self.request.GET.get("curso_id", "")
        return context
