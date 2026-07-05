from django.db import models
from django.urls import reverse


class Estudiante(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    apellido = models.CharField("Apellido", max_length=100)
    email = models.EmailField("Correo electrónico", unique=True)
    curso = models.ForeignKey(
        "cursos.Curso",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="estudiantes",
        verbose_name="Curso",
    )
    fecha_registro = models.DateTimeField("Fecha de registro", auto_now_add=True)
    activo = models.BooleanField("Activo", default=True)

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def get_absolute_url(self):
        return reverse("estudiantes:lista")
