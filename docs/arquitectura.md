# Arquitectura del sistema

El sistema **Control de Estudiantes** sigue el patrón **MTV** (Model-Template-View)
propio de Django.

## Componentes principales

```
config/          Configuración global (settings, urls, wsgi)
estudiantes/     App principal (CRUD de estudiantes)
  models.py      Modelo Estudiante
  views.py       Vistas basadas en clases (CBVs)
  forms.py       EstudianteForm (ModelForm)
  mixins.py      BusquedaMixin, FiltroCursoMixin (V2)
  templates/     Plantillas HTML
cursos/          App secundaria (modelo Curso)
reportes/        App de exportación PDF/Excel (solo V2)
```

## Flujo de una petición

1. El navegador solicita una URL.
2. `config/urls.py` la enruta a la app correspondiente.
3. La **vista** (CBV) consulta el **modelo** vía el ORM de Django.
4. La **plantilla** recibe el contexto y genera el HTML.
5. Django devuelve la respuesta al navegador.

## Base de datos

- Desarrollo: **SQLite** (sin configuración).
- Producción: **PostgreSQL** (definiendo `DATABASE_URL`).

## Decisiones de diseño

- Uso de **vistas basadas en clases** para maximizar la reutilización.
- **Mixins** componibles para búsqueda y filtrado.
- Separación de responsabilidades en apps independientes.
