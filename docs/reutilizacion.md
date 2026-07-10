# Reutilización de software

Este documento detalla los componentes reutilizables del proyecto (punto 6 del
proyecto integrador).

## Funciones y clases reutilizadas

| Componente | Ubicación | Cómo se reutiliza |
|------------|-----------|-------------------|
| CBVs genéricas de Django | `estudiantes/views.py` | `ListView`, `CreateView`, `UpdateView`, `DeleteView` proveen el CRUD sin escribir lógica manual. |
| `BusquedaMixin` | `estudiantes/mixins.py` | Agrega búsqueda por texto a cualquier `ListView` declarando `search_fields`. |
| `FiltroCursoMixin` | `estudiantes/mixins.py` | Filtro por curso componible con la búsqueda. |
| `EstudianteForm` | `estudiantes/forms.py` | Un único `ModelForm` usado por Create y Update. |
| `_tabla_estudiantes.html` | `templates/.../partials/` | La tabla se define una vez y se incluye con `{% include %}`. |
| Modelo `Estudiante` | `estudiantes/models.py` | La app `reportes` lo **importa** en lugar de duplicarlo. |

## Patrones aplicados

- **Mixin:** para inyectar comportamiento (búsqueda, filtro) sin herencia rígida.
- **Template Method:** las CBVs de Django definen el esqueleto y nosotros
  sobrescribimos métodos puntuales (`get_context_data`, `get_queryset`).
- **DRY (Don't Repeat Yourself):** un solo formulario y una sola plantilla de tabla.

## Reutilización en otros proyectos

Los mixins y las CBVs genéricas pueden copiarse a cualquier otro proyecto Django
que necesite listados con búsqueda y filtros, sin modificaciones.
