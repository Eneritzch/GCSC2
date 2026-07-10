"""Puebla la base con cursos, estudiantes y superusuario. Uso: manage.py seed_datos."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from cursos.models import Curso
from estudiantes.models import Estudiante

User = get_user_model()

CURSOS = [
    ("Matemáticas", "MAT-101"),
    ("Programación", "PRO-102"),
    ("Historia", "HIS-201"),
    ("Física", "FIS-301"),
    ("Diseño Gráfico", "DIS-105"),
]

ESTUDIANTES = [
    ("Ana", "Pérez", "ana.perez@example.com", "MAT-101", True),
    ("Luis", "Gómez", "luis.gomez@example.com", "PRO-102", True),
    ("María", "López", "maria.lopez@example.com", "HIS-201", True),
    ("Carlos", "Rodríguez", "carlos.rodriguez@example.com", "FIS-301", False),
    ("Sofía", "Martínez", "sofia.martinez@example.com", "DIS-105", True),
    ("Diego", "Andrade", "diego.andrade@example.com", "PRO-102", True),
    ("Valentina", "Torres", "valentina.torres@example.com", "MAT-101", True),
    ("Jorge", "Vega", "jorge.vega@example.com", "HIS-201", False),
    ("Camila", "Suárez", "camila.suarez@example.com", "DIS-105", True),
    ("Andrés", "Mora", "andres.mora@example.com", "FIS-301", True),
    ("Daniela", "Castro", "daniela.castro@example.com", "PRO-102", True),
    ("Mateo", "Jiménez", "mateo.jimenez@example.com", "MAT-101", False),
    ("Lucía", "Ramírez", "lucia.ramirez@example.com", "HIS-201", True),
    ("Sebastián", "Paredes", "sebastian.paredes@example.com", "FIS-301", True),
    ("Isabella", "Cedeño", "isabella.cedeno@example.com", "DIS-105", True),
    ("Nicolás", "Herrera", "nicolas.herrera@example.com", "PRO-102", True),
]

# Credenciales del superusuario por defecto.
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@gcsc.com"
ADMIN_PASSWORD = "admin1234"


class Command(BaseCommand):
    help = "Crea superusuario, cursos y estudiantes de ejemplo (idempotente)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Elimina estudiantes y cursos antes de poblar.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            Estudiante.objects.all().delete()
            Curso.objects.all().delete()
            self.stdout.write("Datos previos eliminados.")

        # --- Superusuario ---
        if User.objects.filter(username=ADMIN_USERNAME).exists():
            self.stdout.write(f"Superusuario '{ADMIN_USERNAME}' ya existe.")
        else:
            User.objects.create_superuser(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superusuario creado: {ADMIN_USERNAME} / {ADMIN_PASSWORD}"
                )
            )

        # --- Cursos ---
        cursos = {}
        for nombre, codigo in CURSOS:
            curso, _ = Curso.objects.get_or_create(
                codigo=codigo, defaults={"nombre": nombre}
            )
            cursos[codigo] = curso

        # --- Estudiantes ---
        creados = 0
        for nombre, apellido, email, codigo, activo in ESTUDIANTES:
            _, creado = Estudiante.objects.get_or_create(
                email=email,
                defaults={
                    "nombre": nombre,
                    "apellido": apellido,
                    "curso": cursos[codigo],
                    "activo": activo,
                },
            )
            creados += int(creado)

        self.stdout.write(
            self.style.SUCCESS(
                f"Listo: {Curso.objects.count()} cursos y "
                f"{Estudiante.objects.count()} estudiantes "
                f"({creados} nuevos)."
            )
        )
