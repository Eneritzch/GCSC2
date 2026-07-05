"""
Vistas de la app reportes.

Reutiliza el modelo Estudiante (lo importa, no lo duplica) y el MISMO patrón de
filtrado por ``?q=`` y ``?curso_id=`` que la lista de estudiantes, demostrando
reutilización de lógica entre apps.
"""

from django.db.models import Q
from django.http import HttpResponse

from estudiantes.models import Estudiante

from .utils import generar_excel, generar_pdf

# Mismos campos de búsqueda que EstudianteListView.search_fields (reutilización).
SEARCH_FIELDS = ["nombre", "apellido", "email"]


def estudiantes_filtrados(request):
    """
    Devuelve el queryset de estudiantes aplicando los filtros de la URL.

    Comparte los parámetros ?q= y ?curso_id= con la lista de estudiantes, de
    modo que un reporte respeta exactamente lo que el usuario está viendo.
    """
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
    """Genera un PDF con los estudiantes (respetando filtros)."""
    estudiantes = estudiantes_filtrados(request)
    contenido = generar_pdf(estudiantes)
    respuesta = HttpResponse(contenido, content_type="application/pdf")
    respuesta["Content-Disposition"] = 'attachment; filename="estudiantes.pdf"'
    return respuesta


def reporte_excel(request):
    """Genera un .xlsx con los estudiantes (respetando filtros)."""
    estudiantes = estudiantes_filtrados(request)
    contenido = generar_excel(estudiantes)
    respuesta = HttpResponse(
        contenido,
        content_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )
    respuesta["Content-Disposition"] = 'attachment; filename="estudiantes.xlsx"'
    return respuesta
