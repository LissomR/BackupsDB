# Copilot Instructions

Este proyecto es un sistema automático de backup de bases de datos PostgreSQL con integración a Google Drive.

## Estructura Principal

El proyecto utiliza un arquitectura modular con los siguientes componentes:

1. **backup.py** - Maneja la creación de backups de PostgreSQL
2. **google_drive.py** - Integración con Google Drive
3. **scheduler.py** - Orquestador principal con planificación de tareas

## Configuración Inicial

Antes de ejecutar:

1. Instalar dependencias: `pip install -r requirements.txt`
2. Copiar y configurar: `cp .env.example .env`
3. Llenar credenciales necesarias en `.env`
4. Preparar `credentials.json` para Google Drive

## Ejecución

```bash
python src/scheduler.py
```

El sistema ejecutará automáticamente un backup diario en la hora especificada en `.env`.

## Variables de Entorno Necesarias

- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` - PostgreSQL
- `GOOGLE_DRIVE_FOLDER_ID`, `GOOGLE_CREDENTIALS_FILE` - Google Drive
- `BACKUP_HOUR`, `BACKUP_MINUTE` - Horario de backup

## Seguridad

- Nunca commitar `.env` o `credentials.json`
- Usar tokens con permisos limitados
- Mantener credenciales en archivos seguros

## Despliegue en Railway

El proyecto incluye un `Procfile` para desplegar en Railway:
- Railway ejecutará automáticamente `python src/scheduler.py`
- Configura todas las variables de entorno en el dashboard de Railway
- El backup se ejecutará según el horario especificado en `BACKUP_HOUR` y `BACKUP_MINUTE`

