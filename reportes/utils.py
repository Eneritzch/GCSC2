"""
Utilidades de generación de reportes (PDF y Excel).

Estas funciones son puras respecto a Django: reciben un queryset/iterable de
Estudiante y devuelven los bytes del archivo. Así se reutiliza la misma lógica
de armado desde cualquier vista y se puede testear con facilidad.
"""

import io

from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet

# Encabezados compartidos por ambos formatos (reutilización).
COLUMNAS = ["Nombre", "Apellido", "Email", "Curso"]


def _filas(estudiantes):
    """Convierte los estudiantes en filas de texto para los reportes."""
    for est in estudiantes:
        yield [
            est.nombre,
            est.apellido,
            est.email,
            est.curso.nombre if est.curso else "—",
        ]


def generar_pdf(estudiantes):
    """Genera un PDF con la lista de estudiantes y devuelve los bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        title="Reporte de Estudiantes",
    )
    estilos = getSampleStyleSheet()
    elementos = [
        Paragraph("Reporte de Estudiantes", estilos["Title"]),
        Spacer(1, 0.5 * cm),
    ]

    data = [COLUMNAS] + list(_filas(estudiantes))
    tabla = Table(data, repeatRows=1)
    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#f2f2f2")],
                ),
            ]
        )
    )
    elementos.append(tabla)
    doc.build(elementos)

    buffer.seek(0)
    return buffer.getvalue()


def generar_excel(estudiantes):
    """Genera un .xlsx con la lista de estudiantes y devuelve los bytes."""
    buffer = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Estudiantes"

    # Encabezados en negrita.
    ws.append(COLUMNAS)
    for celda in ws[1]:
        celda.font = Font(bold=True)

    for fila in _filas(estudiantes):
        ws.append(fila)

    # Ancho de columnas cómodo.
    anchos = [18, 18, 32, 20]
    for i, ancho in enumerate(anchos, start=1):
        ws.column_dimensions[chr(64 + i)].width = ancho

    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
