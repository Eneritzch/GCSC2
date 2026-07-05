from django.test import TestCase
from django.urls import reverse

from cursos.models import Curso
from estudiantes.models import Estudiante


class ReportesTests(TestCase):
    """Tests de la app reportes (exportación y reutilización de filtros)."""

    def setUp(self):
        self.mate = Curso.objects.create(nombre="Matemáticas", codigo="MAT-101")
        self.hist = Curso.objects.create(nombre="Historia", codigo="HIS-201")
        Estudiante.objects.create(
            nombre="Ana", apellido="Pérez", email="ana@example.com", curso=self.mate
        )
        Estudiante.objects.create(
            nombre="Luis", apellido="Gómez", email="luis@example.com", curso=self.hist
        )

    def test_reporte_pdf_responde_pdf(self):
        respuesta = self.client.get(reverse("reportes:pdf"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta["Content-Type"], "application/pdf")
        # Un PDF válido empieza con la firma %PDF.
        self.assertTrue(respuesta.content.startswith(b"%PDF"))

    def test_reporte_excel_responde_xlsx(self):
        respuesta = self.client.get(reverse("reportes:excel"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("spreadsheetml", respuesta["Content-Type"])
        # Un .xlsx es un ZIP: empieza con la firma PK.
        self.assertTrue(respuesta.content.startswith(b"PK"))

    def test_reporte_reutiliza_filtro_curso(self):
        """El reporte respeta el filtro ?curso_id= igual que la lista."""
        from reportes.views import estudiantes_filtrados

        request = self.client.get(
            reverse("reportes:pdf"), {"curso_id": self.mate.pk}
        ).wsgi_request
        queryset = estudiantes_filtrados(request)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().nombre, "Ana")


class BusquedaFiltroTests(TestCase):
    """Tests de los mixins de búsqueda y filtro sobre la lista (V2)."""

    def setUp(self):
        self.mate = Curso.objects.create(nombre="Matemáticas", codigo="MAT-101")
        self.hist = Curso.objects.create(nombre="Historia", codigo="HIS-201")
        Estudiante.objects.create(
            nombre="Ana", apellido="Pérez", email="ana@example.com", curso=self.mate
        )
        Estudiante.objects.create(
            nombre="Luis", apellido="Gómez", email="luis@example.com", curso=self.hist
        )

    def test_busqueda_por_texto(self):
        respuesta = self.client.get(reverse("estudiantes:lista"), {"q": "Ana"})
        self.assertContains(respuesta, "Ana")
        self.assertNotContains(respuesta, "Gómez")

    def test_filtro_por_curso(self):
        respuesta = self.client.get(
            reverse("estudiantes:lista"), {"curso_id": self.hist.pk}
        )
        self.assertContains(respuesta, "Gómez")
        self.assertNotContains(respuesta, "Pérez")
