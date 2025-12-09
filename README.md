# Backup Database Automation

Este proyecto automatiza backups diarios de una base de datos PostgreSQL y los sube a Google Drive y GitHub.

## Características

- **Backup Automático Diario**: Programa backups de PostgreSQL según horario configurado
- **Google Drive Integration**: Sube automáticamente los backups a tu Google Drive
- **GitHub Integration**: Almacena copias de los backups en tu repositorio GitHub
- **Logging Completo**: Registra todas las operaciones en archivos de log

## Requisitos

- Python 3.8+
- PostgreSQL instalado y ejecutándose
- Cuenta de Google (para Google Drive)
- Token de acceso de GitHub
- Git instalado

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd /home/luis/BackupsDB
```

### 2. Crear un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar el archivo de ejemplo y completar la configuración:

```bash
cp .env.example .env
```

Editar `.env` con tus datos:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña

GOOGLE_DRIVE_FOLDER_ID=tu_id_carpeta_google_drive
GOOGLE_CREDENTIALS_FILE=credentials.json

GITHUB_TOKEN=tu_token_github
GITHUB_REPO_OWNER=tu_usuario_github
GITHUB_REPO_NAME=nombre_repo

BACKUP_HOUR=2
BACKUP_MINUTE=0
```

### 5. Configurar Google Drive (Opcional)

Para usar Google Drive, necesitas un archivo `credentials.json`:

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear un nuevo proyecto
3. Activar la API de Google Drive
4. Crear una credencial de servicio o cuenta de servicio
5. Descargar el JSON y guardarlo como `credentials.json`

### 6. Configurar GitHub

1. Generar un token de acceso personal en [GitHub Settings](https://github.com/settings/tokens)
2. Asegurar permisos de `repo` y `workflow`
3. Establecer el token en la variable `GITHUB_TOKEN` del archivo `.env`

## Uso

### Ejecutar el scheduler

```bash
python src/scheduler.py
```

### Ejecutar un backup manual

```bash
python -c "from src.backup import PostgreSQLBackup; backup = PostgreSQLBackup(); backup.create_backup()"
```

### Ver logs

```bash
tail -f logs/backup_$(date +%Y%m%d).log
```

## Ejecutar en Segundo Plano (Linux/Mac)

### Con systemd (recomendado)

Crear archivo `/etc/systemd/system/backup-scheduler.service`:

```ini
[Unit]
Description=PostgreSQL Backup Scheduler
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/home/luis/BackupsDB
ExecStart=/home/luis/BackupsDB/venv/bin/python src/scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activar el servicio:

```bash
sudo systemctl enable backup-scheduler
sudo systemctl start backup-scheduler
sudo systemctl status backup-scheduler
```

### Con nohup (alternativa simple)

```bash
nohup python src/scheduler.py > logs/scheduler.log 2>&1 &
```

## Estructura del Proyecto

```
/home/luis/BackupsDB/
├── src/
│   ├── backup.py              # Módulo de backup PostgreSQL
│   ├── google_drive.py        # Módulo de Google Drive
│   ├── github_uploader.py     # Módulo de GitHub
│   └── scheduler.py           # Scheduler principal
├── config/                    # Archivos de configuración
├── logs/                      # Logs del sistema
├── backups/                   # Backups locales (temporal)
├── requirements.txt           # Dependencias de Python
├── .env.example              # Ejemplo de variables de entorno
├── .gitignore                # Archivos a ignorar en Git
└── README.md                 # Este archivo
```

## Configuración de Cron (Alternativa)

Si prefieres usar cron en lugar del scheduler de Python:

```bash
crontab -e
```

Agregar la línea (para ejecutar a las 2:00 AM):

```
0 2 * * * cd /home/luis/BackupsDB && /home/luis/BackupsDB/venv/bin/python src/scheduler.py >> logs/cron.log 2>&1
```

## Solución de Problemas

### Error de conexión a PostgreSQL
- Verificar que PostgreSQL esté ejecutándose
- Verificar credenciales en `.env`
- Verificar que pg_dump está instalado: `which pg_dump`

### Error de autenticación en Google Drive
- Verificar que `credentials.json` existe y es válido
- Verificar que la carpeta ID en Google Drive es correcta
- Verificar permisos de la cuenta de servicio

### Error de autenticación en GitHub
- Verificar que el token no ha expirado
- Verificar que el token tiene permisos suficientes
- Verificar que el repositorio existe

## Logs y Monitoreo

Los logs se guardan en:
- `logs/backup_YYYYMMDD.log` - Logs diarios del scheduler
- `logs/` - Todos los archivos de log

Comando para ver logs en tiempo real:

```bash
tail -f logs/backup_$(date +%Y%m%d).log
```

## Licencia

Este proyecto es de código abierto. Úsalo libremente.

## Soporte

Para más información sobre las librerías utilizadas:
- [psycopg2](https://www.psycopg.org/)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
- [PyGithub](https://pygithub.readthedocs.io/)
- [schedule](https://schedule.readthedocs.io/)
