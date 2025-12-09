# Copilot Instructions

Este proyecto es un sistema automático de backup de bases de datos PostgreSQL con integración a AWS S3.

## Estructura Principal

El proyecto utiliza un arquitectura modular con los siguientes componentes:

1. **backup.py** - Maneja la creación de backups de PostgreSQL usando psycopg2
2. **s3_uploader.py** - Integración con AWS S3
3. **scheduler.py** - Orquestador principal con planificación de tareas

## Configuración Inicial

Antes de ejecutar:

1. Instalar dependencias: `pip install -r requirements.txt`
2. Copiar y configurar: `cp .env.example .env`
3. Llenar credenciales necesarias en `.env`
4. Configurar credenciales AWS (Access Key y Secret Key)

## Ejecución

```bash
python src/scheduler.py
```

El sistema ejecutará automáticamente un backup diario en la hora especificada en `.env`.

## Variables de Entorno Necesarias

- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` - PostgreSQL
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `AWS_S3_BUCKET_NAME` - AWS S3
- `BACKUP_HOUR`, `BACKUP_MINUTE` - Horario de backup

## Seguridad

- Nunca commitar `.env`
- Usar credenciales AWS con permisos limitados (solo S3)
- Mantener credenciales en archivos seguros

## Despliegue en Railway

El proyecto incluye un `Procfile` para desplegar en Railway:
- Railway ejecutará automáticamente `python src/scheduler.py`
- Configura todas las variables de entorno en el dashboard de Railway
- El backup se ejecutará según el horario especificado en `BACKUP_HOUR` y `BACKUP_MINUTE`

