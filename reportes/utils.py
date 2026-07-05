"""Generacion de reportes de estudiantes en PDF y Excel."""

import io

from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

COLUMNAS = ["Nombre", "Apellido", "Email", "Curso"]


def _filas(estudiantes):
    for est in estudiantes:
        yield [
            est.nombre,
            est.apellido,
            est.email,
            est.curso.nombre if est.curso else "-",
        ]


def generar_pdf(estudiantes):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Reporte de Estudiantes")
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
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#212529")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    elementos.append(tabla)
    doc.build(elementos)

    buffer.seek(0)
    return buffer.getvalue()


def generar_excel(estudiantes):
    buffer = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Estudiantes"

    ws.append(COLUMNAS)
    for celda in ws[1]:
        celda.font = Font(bold=True)

    for fila in _filas(estudiantes):
        ws.append(fila)

    anchos = [18, 18, 32, 20]
    for i, ancho in enumerate(anchos, start=1):
        ws.column_dimensions[chr(64 + i)].width = ancho

    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
