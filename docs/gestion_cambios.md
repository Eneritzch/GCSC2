# Documento de Gestión de Cambios

**Proyecto:** Control de Estudiantes
**Asignatura:** Gestión de la Configuración de Software
**Repositorio:** https://github.com/Eneritzch/GCSC2
**Integrantes:** 4

Este documento registra formalmente las **solicitudes de cambio (SC)** que
dieron origen a la evolución del sistema de la versión **V1** (rama `main`) a la
versión **V2** (rama `feature/v2-busqueda-reportes`). Cada cambio fue evaluado,
aprobado e implementado siguiendo el proceso de control de cambios.

## Integrantes y roles de exposición

Grupo de 4 integrantes. Los temas de la exposición individual se distribuyen así:

| # | Integrante | Usuario GitHub | Tema de exposición |
|---|---|---|---|
| 1 | [Jaione Cherres] | [Eneritzch] | Gestión del cambio |
| 2 | [Dulce Villacis] | [DullVillacis] | Gestión de versiones (Git/GitHub) |
| 3 | [Ronny Arellano] | [RonnyAreMC] | Integración continua y Despliegue continuo |
| 4 | [Elias Ramos] | [eliasDniel] | Reutilización y variabilidad |

## Tabla de control de cambios

| # | Cambio solicitado | Motivo | Responsable | Fecha solicitud | Fecha aprobación | Estado | Versión afectada |
|---|---|---|---|---|---|---|---|
| 1 | Agregar búsqueda de estudiantes por nombre/apellido/email | El cliente necesitaba encontrar estudiantes rápidamente en listas grandes | [Dulce Villacis] | 2026-06-15 | 2026-06-16 | Implementado | V1 → V2 |
| 2 | Agregar exportación a PDF y Excel | Coordinación académica necesita reportes físicos para archivo institucional | [Elias Ramos] | 2026-06-18 | 2026-06-19 | Implementado | V2 |
| 3 | Agregar filtro por curso | Facilitar la gestión cuando hay múltiples cursos simultáneos | [Jaione Cherres] | 2026-06-20 | 2026-06-21 | Implementado | V2 |

> Aprobación de los cambios a cargo de [Ronny Arellano] (responsable de
> versiones e integración).

## Detalle de implementación

### SC-1 — Búsqueda por texto
- **Solución técnica:** se creó `BusquedaMixin` en `estudiantes/mixins.py`, un
  mixin genérico reutilizable. `EstudianteListView` pasó de heredar de
  `ListView` a heredar de `(BusquedaMixin, FiltroCursoMixin, ListView)`,
  agregando únicamente el atributo `search_fields`.
- **Impacto en el código:** mínimo (una línea de herencia + un atributo),
  demostrando reutilización sin reescritura.

### SC-2 — Exportación a PDF y Excel
- **Solución técnica:** nueva app `reportes/` que **importa** el modelo
  `Estudiante` (no lo duplica). La generación de archivos vive en
  `reportes/utils.py` (`reportlab` para PDF, `openpyxl` para Excel).
- **Impacto en el código:** aditivo; no modifica la app `estudiantes` salvo por
  los botones de exportación en la plantilla de lista.

### SC-3 — Filtro por curso
- **Solución técnica:** `FiltroCursoMixin` en `estudiantes/mixins.py`, componible
  con `BusquedaMixin`. Reutiliza el mismo patrón de lectura de querystring
  (`?curso_id=`). Los reportes reutilizan el mismo filtro.
- **Impacto en el código:** mínimo y componible.

## Trazabilidad

| SC | Rama | Commit(s) representativo(s) |
|----|------|------------------------------|
| 1 | `feature/v2-busqueda-reportes` | `feat(v2): agregar BusquedaMixin reutilizable con búsqueda por texto` |
| 3 | `feature/v2-busqueda-reportes` | `feat(v2): agregar filtro por curso` |
| 2 | `feature/v2-busqueda-reportes` | `feat(v2): app reportes con exportación a PDF y Excel` |
