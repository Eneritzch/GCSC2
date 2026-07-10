# Guía de contribución

Este proyecto usa un flujo de trabajo basado en ramas.

## Flujo de trabajo

1. Cada integrante trabaja en su propia rama `feature/<descripcion>`.
2. Los commits siguen la convención [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` nueva funcionalidad
   - `fix:` corrección de un error
   - `docs:` cambios en documentación
   - `test:` agregar o corregir tests
   - `chore:` tareas de mantenimiento
   - `refactor:` reorganización de código sin cambiar comportamiento
3. Antes de subir código: ejecutar `make lint` y `make test`.
4. Abrir un Pull Request hacia `main` para revisión.
5. La Integración Continua (GitHub Actions) debe pasar en verde.

## Estilo de código

- Python: se valida con `flake8` (ver `.flake8`).
- Longitud máxima de línea: 100 caracteres.
