"""Filtros de plantilla para la interfaz."""

from django import template

register = template.Library()

# Paleta de tonos de azul para los avatares (sin degradados, colores solidos).
PALETA_AZUL = [
    "#2563eb",
    "#0ea5e9",
    "#4f46e5",
    "#0284c7",
    "#3b82f6",
    "#6366f1",
    "#0891b2",
    "#1d4ed8",
]


@register.filter
def avatar_color(value):
    """Devuelve un color de la paleta segun el id (variedad estable por estudiante)."""
    try:
        indice = int(value) % len(PALETA_AZUL)
    except (TypeError, ValueError):
        indice = 0
    return PALETA_AZUL[indice]


@register.filter
def iniciales(estudiante):
    """Iniciales del estudiante para el avatar."""
    nombre = (estudiante.nombre or " ")[0]
    apellido = (estudiante.apellido or " ")[0]
    return (nombre + apellido).upper()
