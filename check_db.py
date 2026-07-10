import os
import sys
import socket
from urllib.parse import urlparse

print("=== DIAGNÓSTICO DE BASE DE DATOS ===")
db_url = os.environ.get("DATABASE_URL", "")
if not db_url:
    print("DATABASE_URL no está definida. Usando SQLite por defecto.")
    sys.exit(0)

print(f"DATABASE_URL detectada.")
try:
    parsed = urlparse(db_url)
    scheme = parsed.scheme
    host = parsed.hostname
    port = parsed.port or (5432 if "postgres" in scheme else None)
    username = parsed.username
    database = parsed.path.lstrip('/')
    
    print(f"Esquema: {scheme}")
    print(f"Host: {host}")
    print(f"Puerto: {port}")
    print(f"Usuario: {username}")
    print(f"Base de datos: {database}")
    
    if host:
        print(f"Intentando conexión TCP a {host}:{port} con timeout de 5 segundos...")
        s = socket.create_connection((host, port), timeout=5)
        print("✅ Conexión TCP exitosa a la base de datos.")
        s.close()
    else:
        print("❌ No se pudo extraer el host de la DATABASE_URL.")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error al conectar al host de la base de datos: {e}")
    sys.exit(1)

print("=== INICIANDO DJANGO SYSTEM CHECK ===")
try:
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    from django.db import connections
    from django.db.utils import OperationalError
    
    print("Intentando consulta de prueba en la base de datos...")
    conn = connections['default']
    # Forzar conexión
    conn.ensure_connection()
    print("✅ Django pudo conectarse correctamente a la base de datos PostgreSQL.")
except OperationalError as oe:
    print(f"❌ Django no pudo establecer conexión operacional: {oe}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error inesperado cargando Django: {e}")
    sys.exit(1)

print("=== DIAGNÓSTICO EXITOSO ===")
sys.exit(0)
