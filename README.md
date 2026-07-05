# Control de Estudiantes

[![CI](https://github.com/Eneritzch/GCSC2/actions/workflows/ci.yml/badge.svg)](https://github.com/Eneritzch/GCSC2/actions/workflows/ci.yml)

Sistema web para el registro y control de estudiantes, desarrollado con
Django 5. Es el Proyecto Final Integrador de la asignatura Gestión de la
Configuración de Software y demuestra:

- Control de versiones con Git (dos versiones en dos ramas).
- Control de cambios documentado (`docs/gestion_cambios.md`).
- Reutilización de código (CBVs genéricas, mixins, formularios, componentes de
  plantilla y un modelo compartido entre apps).
- Variabilidad entre una versión básica (V1) y una ampliada (V2).
- Integración continua (CI) con GitHub Actions.
- Despliegue (CD) en Render.

Demo desplegada: _(completar con la URL de Render)_

## Estructura del proyecto

```
config/          Settings, URLs y WSGI del proyecto
estudiantes/     App principal: CRUD de estudiantes (V1)
  mixins.py      BusquedaMixin y FiltroCursoMixin (V2)
cursos/          App secundaria: modelo Curso
reportes/        App nueva en V2: exporta PDF/Excel
docs/            Documento de gestión de cambios
.github/workflows/ci.yml   Integración continua
Procfile / render.yaml     Despliegue en Render
manage.py
```

## Instalación local

Requisitos: Python 3.11+ y Git.

```bash
git clone https://github.com/Eneritzch/GCSC2.git
cd GCSC2

python -m venv venv
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

pip install -r requirements-dev.txt

copy .env.example .env        # Linux/macOS: cp .env.example .env

python manage.py migrate
python manage.py createsuperuser   # opcional, para el admin
python manage.py runserver
```

Abrir http://127.0.0.1:8000/ en el navegador.

## Base de datos

Por defecto se usa SQLite (no requiere configuración). Para usar PostgreSQL,
define `DATABASE_URL` en el `.env`:

```
DATABASE_URL=postgres://usuario:clave@localhost:5432/control_estudiantes
```

Luego ejecuta `python manage.py migrate`. En producción (Render) la SSL se
activa automáticamente; en local se omite.

## Estructura de ramas

| Rama                           | Versión | Contenido                                          |
|--------------------------------|---------|----------------------------------------------------|
| `main`                         | V1      | CRUD básico de estudiantes con CBVs genéricas.     |
| `feature/v2-busqueda-reportes` | V2      | Búsqueda, filtro por curso y exportación PDF/Excel.|

La V2 se construyó modificando el mínimo código posible sobre la V1, para que el
diff de GitHub evidencie cómo la reutilización permite extender la funcionalidad
sin reescribir lo existente.

## Tabla comparativa V1 vs V2

| Característica                   | V1 (`main`) | V2 (`feature/v2-busqueda-reportes`) |
|---------------------------------|:-----------:|:-----------------------------------:|
| CRUD de estudiantes (CBVs)      | Sí          | Sí                                  |
| Paginación                      | Sí          | Sí                                  |
| Relación Estudiante-Curso       | Sí          | Sí                                  |
| Panel de administración         | Sí          | Sí                                  |
| Tests unitarios + CI            | Sí          | Sí                                  |
| Búsqueda por texto (`?q=`)      | No          | Sí (`BusquedaMixin`)                |
| Filtro por curso (`?curso_id=`) | No          | Sí (`FiltroCursoMixin`)             |
| Exportar a PDF                  | No          | Sí (app `reportes`)                 |
| Exportar a Excel                | No          | Sí (app `reportes`)                 |

## Componentes reutilizables

1. CBVs genéricas de Django (`ListView`, `CreateView`, `UpdateView`,
   `DeleteView`): todo el CRUD se apoya en clases del framework.
2. `BusquedaMixin` (`estudiantes/mixins.py`): agrega búsqueda por texto a
   cualquier `ListView` declarando `search_fields`. Se activa con `?q=`.
3. `FiltroCursoMixin` (`estudiantes/mixins.py`): filtrado por curso vía
   `?curso_id=`, componible con `BusquedaMixin`.
4. `EstudianteForm` (`ModelForm`): un único formulario reutilizado por
   `CreateView` y `UpdateView`.
5. `_tabla_estudiantes.html`: la tabla se define una vez y se incluye con
   `{% include %}`.
6. Modelo `Estudiante` compartido: `reportes` lo importa en lugar de duplicarlo.

## Tests

```bash
python manage.py test
# o
pytest
```

Cubren creación, validación de email único, listado, edición, borrado,
búsqueda, filtro y exportación.

## Despliegue en Render

El proyecto incluye `render.yaml` (Blueprint) y `Procfile`. Render ejecuta:

- Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start: `gunicorn config.wsgi --log-file -`

Las variables `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` y `DATABASE_URL` se
configuran en el panel de Render. Los archivos estáticos se sirven con WhiteNoise.

## Documentación adicional

- `docs/gestion_cambios.md`: registro formal de las solicitudes de cambio que
  dieron origen a la V2.

## Autoría

Proyecto académico - Gestión de la Configuración de Software.
