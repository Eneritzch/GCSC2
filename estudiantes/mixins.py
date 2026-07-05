"""
Mixins reutilizables para las vistas de la app estudiantes.

Estos mixins son GENÉRICOS: no dependen del modelo Estudiante y pueden
aplicarse a cualquier ``ListView`` declarando los atributos correspondientes.
Demuestran cómo extender funcionalidad reutilizando el patrón de mixins de
Django sin reescribir las vistas.
"""

from django.db.models import Q


class BusquedaMixin:
    """
    Agrega capacidad de búsqueda por texto a cualquier ListView.

    Se activa leyendo el parámetro ``?q=`` de la URL. Cada vista que lo use
    define en ``search_fields`` los campos sobre los que buscar.
    """

    search_fields = []  # cada vista define en qué campos buscar

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
        # Se expone el término buscado para conservarlo en el input y en la
        # paginación.
        context["q"] = self.request.GET.get("q", "")
        return context


class FiltroCursoMixin:
    """
    Agrega filtrado por curso a cualquier ListView mediante ``?curso_id=``.

    Sigue el mismo patrón que ``BusquedaMixin`` y es componible con él: basta
    con listar ambos mixins antes de la vista base.
    """

    curso_field = "curso_id"  # nombre del campo FK en el modelo

    def get_queryset(self):
        queryset = super().get_queryset()
        curso_id = self.request.GET.get("curso_id")
        if curso_id:
            queryset = queryset.filter(**{self.curso_field: curso_id})
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Se importa aquí para evitar dependencias circulares entre apps.
        from cursos.models import Curso

        context["cursos"] = Curso.objects.all()
        context["curso_id"] = self.request.GET.get("curso_id", "")
        return context
