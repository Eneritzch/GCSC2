"""
Configuración WSGI para el proyecto control_estudiantes.

Expone el callable WSGI como una variable a nivel de módulo llamada
``application``. Usado por Gunicorn en producción.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
