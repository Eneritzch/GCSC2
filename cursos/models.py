from django.db import models


class Curso(models.Model):
    """Curso académico al que pueden pertenecer los estudiantes."""

    nombre = models.CharField("Nombre", max_length=100)
    codigo = models.CharField("Código", max_length=20, unique=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
