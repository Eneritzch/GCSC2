import os
import sys
import subprocess

print("=== INICIANDO SCRIPT DE ARRANQUE (start.py) ===")

# 1. Ejecutar diagnóstico de base de datos
try:
    print("Ejecutando check_db.py...")
    subprocess.run([sys.executable, "check_db.py"], check=True)
    print("✅ Diagnóstico de base de datos exitoso.")
except subprocess.CalledProcessError as e:
    print(f"❌ El diagnóstico de base de datos falló con código {e.returncode}. Abortando arranque.")
    sys.exit(e.returncode)

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
