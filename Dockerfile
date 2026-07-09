# Imagen base ligera de Python.
FROM python:3.11-slim

# Evita archivos .pyc y fuerza salida sin buffer (mejores logs).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependencias primero para aprovechar la cache de Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto.
COPY . .

# Recolecta archivos estaticos.
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Arranca con gunicorn (servidor de produccion).
CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000", "--log-file", "-"]
