import os
import sys
import subprocess

print("=== INICIANDO SCRIPT DE ARRANQUE (start.py) ===")

import socket
from urllib.parse import urlparse

# 1. Ejecutar diagnóstico de base de datos
print("=== DIAGNÓSTICO DE BASE DE DATOS ===")
db_url = os.environ.get("DATABASE_URL", "")
if not db_url:
    print("DATABASE_URL no está definida. Usando SQLite por defecto.")
else:
    try:
        parsed = urlparse(db_url)
        host = parsed.hostname
        port = parsed.port or (5432 if "postgres" in parsed.scheme else None)
        if host:
            print(f"Intentando conexión TCP a {host}:{port} con timeout de 5 segundos...")
            s = socket.create_connection((host, port), timeout=5)
            print("✅ Conexión TCP exitosa a la base de datos.")
            s.close()
    except Exception as e:
        print(f"❌ Error al conectar al host de la base de datos: {e}")
        sys.exit(1)

    print("Intentando consulta de prueba en la base de datos con Django...")
    try:
        import django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
        django.setup()
        from django.db import connections
        from django.db.utils import OperationalError
        conn = connections['default']
        conn.ensure_connection()
        print("✅ Django pudo conectarse correctamente a la base de datos PostgreSQL.")
    except OperationalError as oe:
        print(f"❌ Django no pudo establecer conexión operacional: {oe}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado cargando Django: {e}")
        sys.exit(1)

# 2. Ejecutar collectstatic
try:
    print("Ejecutando collectstatic...")
    # Ejecutamos collectstatic de manera programática usando manage.py
    subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
    print("✅ Collectstatic completado con éxito.")
except subprocess.CalledProcessError as e:
    print(f"❌ Error al ejecutar collectstatic (código {e.returncode}).")
    sys.exit(e.returncode)

# 3. Ejecutar migrate
try:
    print("Ejecutando migraciones (migrate)...")
    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)
    print("✅ Migraciones completadas con éxito.")
except subprocess.CalledProcessError as e:
    print(f"❌ Error al ejecutar las migraciones (código {e.returncode}).")
    sys.exit(e.returncode)

# 4. Iniciar Gunicorn
port = os.environ.get("PORT", "8000")
print(f"Iniciando Gunicorn en el puerto {port}...")

# Comando gunicorn
cmd = [
    "gunicorn",
    "config.wsgi",
    f"--bind=0.0.0.0:{port}",
    "--log-file=-",
    "--access-logfile=-",
    "--workers=2"
]

try:
    # Usamos os.execvp para que Gunicorn reemplace el proceso actual de python
    os.execvp(cmd[0], cmd)
except Exception as e:
    print(f"❌ Error al arrancar Gunicorn: {e}")
    sys.exit(1)
