# Guía de despliegue (CD)

El proyecto se despliega automáticamente en **Render** usando el archivo
`render.yaml` (Blueprint) y el `Procfile`.

## Pasos para desplegar en Render

1. Crear una cuenta en [render.com](https://render.com) y conectar la cuenta de GitHub.
2. Elegir **New > Blueprint** y seleccionar el repositorio `GCSC2`.
3. Render lee `render.yaml` y crea el servicio web automáticamente.
4. Configurar las variables de entorno en el panel:
   - `SECRET_KEY` (generar una nueva y segura)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=.onrender.com`
   - `DATABASE_URL` (si se usa PostgreSQL)
5. Render ejecuta el build y el deploy.

## Comandos que ejecuta Render

- **Build:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start:** `gunicorn config.wsgi --log-file -`

## Despliegue continuo

Cada `git push` a la rama conectada dispara un nuevo despliegue automático.
Los archivos estáticos se sirven con **WhiteNoise**.

## Alternativa con Docker

También se incluye un `Dockerfile` y `docker-compose.yml` para desplegar en
cualquier plataforma que soporte contenedores.
