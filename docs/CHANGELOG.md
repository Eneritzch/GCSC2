# Registro de cambios (Changelog)

Todos los cambios notables del proyecto se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)
y el proyecto usa versionado semántico.

## [2.0.0] - Versión V2 (rama `feature/v2-busqueda-reportes`)

### Agregado
- Búsqueda de estudiantes por texto (`BusquedaMixin`).
- Filtro por curso (`FiltroCursoMixin`).
- App `reportes` con exportación a PDF y Excel.

## [1.0.0] - Versión V1 (rama `main`)

### Agregado
- CRUD de estudiantes con vistas basadas en clases (CBVs).
- Modelos `Estudiante` y `Curso`.
- Panel de administración de Django.
- Tests unitarios e integración continua con GitHub Actions.
- Configuración de despliegue en Render.
