"""Vistas de reportes. Reutilizan el modelo Estudiante y los filtros ?q=/?curso_id=."""

from django.db.models import Q
from django.http import HttpResponse

from estudiantes.models import Estudiante

from .utils import generar_excel, generar_pdf

SEARCH_FIELDS = ["nombre", "apellido", "email"]


def estudiantes_filtrados(request):
    queryset = Estudiante.objects.select_related("curso").all()

    query = request.GET.get("q")
    if query:
        q_objects = Q()
        for field in SEARCH_FIELDS:
            q_objects |= Q(**{f"{field}__icontains": query})
        queryset = queryset.filter(q_objects)

    curso_id = request.GET.get("curso_id")
    if curso_id:
        queryset = queryset.filter(curso_id=curso_id)

    return queryset


def reporte_pdf(request):
    contenido = generar_pdf(estudiantes_filtrados(request))
    respuesta = HttpResponse(contenido, content_type="application/pdf")
    respuesta["Content-Disposition"] = 'attachment; filename="estudiantes.pdf"'
    return respuesta


def reporte_excel(request):
    contenido = generar_excel(estudiantes_filtrados(request))
    respuesta = HttpResponse(
        contenido,
        content_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )
    respuesta["Content-Disposition"] = 'attachment; filename="estudiantes.xlsx"'
    return respuesta
