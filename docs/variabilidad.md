# Variabilidad: V1 vs V2

El proyecto implementa **dos versiones** del mismo sistema para demostrar la
variabilidad (punto 7 del proyecto integrador). Cada versión vive en una rama.

## Versiones

| Rama | Versión | Contenido |
|------|---------|-----------|
| `main` | **V1** | CRUD básico de estudiantes. |
| `feature/v2-busqueda-reportes` | **V2** | V1 + búsqueda + filtro + reportes PDF/Excel. |

## Tabla comparativa

| Característica | V1 | V2 |
|---------------|:--:|:--:|
| CRUD de estudiantes | Sí | Sí |
| Paginación | Sí | Sí |
| Relación Estudiante-Curso | Sí | Sí |
| Panel de administración | Sí | Sí |
| Tests + CI | Sí | Sí |
| Búsqueda por texto | No | Sí |
| Filtro por curso | No | Sí |
| Exportar a PDF | No | Sí |
| Exportar a Excel | No | Sí |

## Cómo se logró la variabilidad

La V2 se construyó **modificando el mínimo código** sobre la V1:

- `EstudianteListView` pasó de heredar de `ListView` a
  `(BusquedaMixin, FiltroCursoMixin, ListView)` — una línea.
- Se agregó la app `reportes` de forma **aditiva**, sin tocar la lógica de V1.

Esto demuestra cómo la **reutilización** permite extender un sistema sin
reescribir lo existente. El `diff` entre ramas evidencia visualmente el cambio.
