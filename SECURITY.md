# Política de seguridad

## Versiones soportadas

| Versión | Soportada |
|---------|-----------|
| 2.0.x   | Sí        |
| 1.0.x   | Sí        |

## Buenas prácticas aplicadas en el proyecto

- Los secretos (`SECRET_KEY`, credenciales de base de datos) se manejan mediante
  variables de entorno y **no** se versionan (ver `.gitignore`).
- `DEBUG=False` en producción.
- `ALLOWED_HOSTS` restringido por variable de entorno.
- Conexión SSL obligatoria a PostgreSQL en producción.

## Reportar una vulnerabilidad

Si encuentras un problema de seguridad, repórtalo de forma privada al equipo
o al docente antes de divulgarlo públicamente.
