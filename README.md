# 🎓 Control de Estudiantes

[![CI](https://github.com/USUARIO/control_estudiantes/actions/workflows/ci.yml/badge.svg)](https://github.com/USUARIO/control_estudiantes/actions/workflows/ci.yml)

Sistema web para el registro y control de estudiantes, desarrollado con
**Django 5**. Es el **Proyecto Final Integrador** de la asignatura
**Gestión de la Configuración de Software** y está diseñado para demostrar, de
forma tangible, prácticas de:

- **Control de versiones** con Git (dos versiones en dos ramas).
- **Control de cambios** documentado (`docs/gestion_cambios.md`).
- **Reutilización de código** (CBVs genéricas, mixins, formularios, componentes
  de plantilla y un modelo compartido entre apps).
- **Variabilidad** entre una versión básica (V1) y una ampliada (V2).
- **Integración continua (CI)** con GitHub Actions.
- **Despliegue (CD)** en Render.

> 🔗 **Demo desplegada:** _(completar con la URL de Render, ej.
> `https://control-estudiantes.onrender.com`)_

---

## 🧱 Estructura del proyecto

```
control_estudiantes/
├── config/          # Settings, URLs y WSGI del proyecto
├── estudiantes/     # App principal: CRUD de estudiantes (V1)
│   ├── mixins.py    # BusquedaMixin y FiltroCursoMixin (V2, reutilizables)
│   └── templates/estudiantes/partials/_tabla_estudiantes.html  # componente reutilizable
├── cursos/          # App secundaria: modelo Curso (relación con Estudiante)
├── reportes/        # App nueva en V2: exporta PDF/Excel reutilizando el modelo Estudiante
├── docs/            # Documento de gestión de cambios
├── .github/workflows/ci.yml   # Integración continua
├── requirements.txt / requirements-dev.txt
├── Procfile / render.yaml     # Despliegue en Render
└── manage.py
```

---

## ⚙️ Instalación local paso a paso

Requisitos: **Python 3.11+** y Git.

```bash
# 1. Clonar el repositorio
git clone https://github.com/USUARIO/control_estudiantes.git
cd control_estudiantes

# 2. Crear y activar un entorno virtual
python -m venv venv
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements-dev.txt

# 4. Configurar variables de entorno
cp .env.example .env        # (Windows: copy .env.example .env)

# 5. Aplicar migraciones
python manage.py migrate

# 6. (Opcional) Crear un superusuario para el admin
python manage.py createsuperuser

# 7. Levantar el servidor
python manage.py runserver
```

Abrir <http://127.0.0.1:8000/> en el navegador.

---

## 🌿 Estructura de ramas (control de versiones)

| Rama                              | Versión | Contenido                                              |
|-----------------------------------|---------|--------------------------------------------------------|
| `main`                            | **V1**  | CRUD básico de estudiantes con CBVs genéricas.         |
| `feature/v2-busqueda-reportes`    | **V2**  | Búsqueda, filtro por curso y exportación PDF/Excel.    |

La V2 se construyó **modificando el mínimo código posible** sobre la V1, para
que el *diff* de GitHub evidencie cómo la reutilización permite extender la
funcionalidad sin reescribir lo existente.

---

## 🔁 Tabla comparativa V1 vs V2

| Característica                       | V1 (`main`) | V2 (`feature/v2-busqueda-reportes`) |
|-------------------------------------|:-----------:|:-----------------------------------:|
| CRUD de estudiantes (CBVs)          | ✅          | ✅                                  |
| Paginación                          | ✅          | ✅                                  |
| Relación Estudiante–Curso           | ✅          | ✅                                  |
| Panel de administración             | ✅          | ✅                                  |
| Tests unitarios + CI                | ✅          | ✅                                  |
| Búsqueda por texto (`?q=`)          | ❌          | ✅ (`BusquedaMixin`)                |
| Filtro por curso (`?curso_id=`)     | ❌          | ✅ (`FiltroCursoMixin`)             |
| Exportar a PDF                      | ❌          | ✅ (app `reportes`)                 |
| Exportar a Excel                    | ❌          | ✅ (app `reportes`)                 |

---

## ♻️ Componentes reutilizables

El proyecto está diseñado alrededor de la reutilización:

1. **CBVs genéricas de Django** (`ListView`, `CreateView`, `UpdateView`,
   `DeleteView`): todo el CRUD se apoya en clases ya provistas por el framework,
   evitando escribir la lógica repetitiva de cada operación.
2. **`BusquedaMixin`** (`estudiantes/mixins.py`): mixin genérico que agrega
   búsqueda por texto a *cualquier* `ListView` declarando `search_fields`. Se
   activa con `?q=` en la URL.
3. **`FiltroCursoMixin`** (`estudiantes/mixins.py`): añade filtrado por curso vía
   `?curso_id=` siguiendo el mismo patrón, componible con `BusquedaMixin`.
4. **`EstudianteForm`** (`ModelForm`): un único formulario reutilizado por
   `CreateView` y `UpdateView` (no se duplica la definición de campos ni la
   validación de email único).
5. **Componente de plantilla `_tabla_estudiantes.html`**: la tabla de
   estudiantes se define una sola vez y se incluye con `{% include %}` tanto en
   la lista principal como en los reportes.
6. **Modelo `Estudiante` compartido**: las apps `estudiantes`, `cursos` y
   `reportes` operan sobre el mismo modelo. `reportes` lo **importa** en lugar de
   duplicarlo, demostrando reutilización de la capa de datos entre apps.

---

## 🧪 Tests

```bash
python manage.py test          # runner de Django
# o
pytest                         # pytest + pytest-django
```

Los tests cubren creación, validación de email único, listado, edición y
borrado de estudiantes.

---

## 🚀 Despliegue en Render

El proyecto incluye `render.yaml` (Blueprint) y `Procfile`. Render ejecuta:

- **Build:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start:** `gunicorn config.wsgi --log-file -`

Las variables `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` y `DATABASE_URL` se
configuran en el panel de Render. Los archivos estáticos se sirven con
**WhiteNoise**.

---

## 📄 Documentación adicional

- [`docs/gestion_cambios.md`](docs/gestion_cambios.md): registro formal de las
  solicitudes de cambio que dieron origen a la V2.

---

## 👥 Autoría

Proyecto académico — Gestión de la Configuración de Software.
