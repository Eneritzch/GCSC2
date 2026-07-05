from django.contrib import admin

from .models import Estudiante


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "email", "curso", "activo", "fecha_registro")
    list_filter = ("activo", "curso")
    search_fields = ("nombre", "apellido", "email")
    list_editable = ("activo",)
    ordering = ("apellido", "nombre")
