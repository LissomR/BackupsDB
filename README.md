# Backup Database Automation

Este proyecto automatiza backups diarios de una base de datos PostgreSQL y los sube automáticamente a Google Drive.

## Características

- **Backup Automático Diario**: Programa backups de PostgreSQL según horario configurado
- **Google Drive Integration**: Sube automáticamente los backups a tu Google Drive
- **Logging Completo**: Registra todas las operaciones en archivos de log
- **Compatible con Railway**: Fácil de desplegar en Railway

## Requisitos

- Python 3.8+
- PostgreSQL instalado y ejecutándose
- Cuenta de Google (para Google Drive)
- Git instalado

## Instalación

### 1. Clonar el proyecto

```bash
git clone https://github.com/LissomR/BackupsDB.git
cd BackupsDB
```

### 2. Crear un entorno virtual

```bash
python3.8 -m venv venv
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

BACKUP_HOUR=2
BACKUP_MINUTE=0
```

### 5. Configurar Google Drive

Para usar Google Drive, necesitas un archivo `credentials.json`:

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear un nuevo proyecto
3. Activar la API de Google Drive
4. Crear una credencial de servicio (Service Account)
5. Descargar el archivo JSON y guardarlo como `credentials.json` en la raíz del proyecto

## Despliegue en Railway

### 1. Crear cuenta en Railway

Ve a [Railway.app](https://railway.app) y crea una cuenta.

### 2. Crear nuevo proyecto

1. Haz clic en "New Project"
2. Selecciona "Deploy from GitHub"
3. Conecta tu repositorio `BackupsDB`

### 3. Configurar variables de entorno en Railway

En el dashboard, ve a **Variables** y añade:

```
DB_HOST=tu_host
DB_PORT=5432
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña

GOOGLE_DRIVE_FOLDER_ID=tu_folder_id
GOOGLE_CREDENTIALS_FILE=credentials.json

BACKUP_HOUR=2
BACKUP_MINUTE=0
```

### 4. Configurar credenciales de Google Drive

Opción A (Recomendado): Usa Railway Secrets
- Ve a la sección de variables
- Copia el contenido completo de tu `credentials.json`
- Pégalo en una variable (puede ser multi-línea)

Opción B: Subir el archivo directamente
- Adjunta el archivo `credentials.json` en la configuración de Railway

### 5. Desplegar

Railway detectará automáticamente el `Procfile` y ejecutará:

```
python src/scheduler.py
```

## Uso

### Ejecutar el scheduler

```bash
python src/scheduler.py
```

### Ejecutar un backup manual

```bash
python -c "from src.backup import PostgreSQLBackup; backup = PostgreSQLBackup(); backup.create_backup()"
```

### Ver logs en tiempo real

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
BackupsDB/
├── src/
│   ├── __init__.py              # Inicializador del módulo
│   ├── backup.py                # Módulo de backup PostgreSQL
│   ├── google_drive.py          # Módulo de Google Drive
│   └── scheduler.py             # Scheduler principal
├── config/                      # Directorio de configuración
├── logs/                        # Logs del sistema
├── backups/                     # Backups locales (temporal)
├── Procfile                     # Configuración para Railway
├── requirements.txt             # Dependencias de Python
├── .env.example                # Ejemplo de variables de entorno
├── .gitignore                  # Archivos a ignorar en Git
└── README.md                   # Este archivo
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

### Error en Railway
- Ver logs en el dashboard de Railway
- Verificar que todas las variables de entorno están configuradas
- Verificar el `Procfile` existe en la raíz

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
- [schedule](https://schedule.readthedocs.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
