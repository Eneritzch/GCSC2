from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from cursos.models import Curso

from .models import Estudiante


class EstudianteModelTests(TestCase):
    """Tests centrados en el modelo Estudiante."""

    def setUp(self):
        self.curso = Curso.objects.create(nombre="Matemáticas", codigo="MAT-101")

    def test_crear_estudiante(self):
        """Se puede crear un estudiante y persiste en la base de datos."""
        estudiante = Estudiante.objects.create(
            nombre="Ana",
            apellido="Pérez",
            email="ana.perez@example.com",
            curso=self.curso,
        )
        self.assertEqual(Estudiante.objects.count(), 1)
        self.assertEqual(str(estudiante), "Ana Pérez")
        self.assertTrue(estudiante.activo)

    def test_email_unico(self):
        """El email debe ser único: un segundo estudiante con el mismo email falla."""
        Estudiante.objects.create(
            nombre="Ana", apellido="Pérez", email="ana@example.com"
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Estudiante.objects.create(
                    nombre="Otra", apellido="Persona", email="ana@example.com"
                )


class EstudianteVistasTests(TestCase):
    """Tests de las Class-Based Views (CRUD)."""

    def setUp(self):
        self.curso = Curso.objects.create(nombre="Historia", codigo="HIS-201")
        self.estudiante = Estudiante.objects.create(
            nombre="Luis",
            apellido="Gómez",
            email="luis.gomez@example.com",
            curso=self.curso,
        )

    def test_listado_estudiantes(self):
        """La vista de lista responde 200 y muestra al estudiante."""
        respuesta = self.client.get(reverse("estudiantes:lista"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Luis")
        self.assertContains(respuesta, "Gómez")

    def test_crear_estudiante_via_vista(self):
        """POST a la vista de creación agrega un estudiante y redirige."""
        datos = {
            "nombre": "María",
            "apellido": "López",
            "email": "maria.lopez@example.com",
            "curso": self.curso.pk,
            "activo": True,
        }
        respuesta = self.client.post(reverse("estudiantes:crear"), datos)
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(
            Estudiante.objects.filter(email="maria.lopez@example.com").exists()
        )

    def test_editar_estudiante_via_vista(self):
        """POST a la vista de edición actualiza los datos del estudiante."""
        datos = {
            "nombre": "Luis Alberto",
            "apellido": "Gómez",
            "email": "luis.gomez@example.com",
            "curso": self.curso.pk,
            "activo": True,
        }
        url = reverse("estudiantes:editar", args=[self.estudiante.pk])
        respuesta = self.client.post(url, datos)
        self.assertEqual(respuesta.status_code, 302)
        self.estudiante.refresh_from_db()
        self.assertEqual(self.estudiante.nombre, "Luis Alberto")

    def test_eliminar_estudiante_via_vista(self):
        """POST a la vista de borrado elimina el estudiante."""
        url = reverse("estudiantes:eliminar", args=[self.estudiante.pk])
        respuesta = self.client.post(url)
        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Estudiante.objects.filter(pk=self.estudiante.pk).exists())
