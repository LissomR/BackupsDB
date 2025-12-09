# Backup Database Automation

Este proyecto automatiza backups diarios de una base de datos PostgreSQL y los sube automáticamente a AWS S3.

## Características

- **Backup Automático Diario**: Programa backups de PostgreSQL según horario configurado
- **AWS S3 Integration**: Sube automáticamente los backups a tu bucket de S3
- **Logging Completo**: Registra todas las operaciones en archivos de log
- **Compatible con Railway**: Fácil de desplegar en Railway

## Requisitos

- Python 3.8+
- PostgreSQL instalado y ejecutándose
- Cuenta de AWS (para S3)
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

AWS_ACCESS_KEY_ID=tu_aws_access_key
AWS_SECRET_ACCESS_KEY=tu_aws_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=tu-bucket-name

BACKUP_HOUR=2
BACKUP_MINUTE=0
```

### 5. Configurar AWS S3

Para usar AWS S3:

1. Ir a [AWS Console](https://console.aws.amazon.com/)
2. Crear un bucket de S3
3. Crear un usuario IAM con permisos de S3 (s3:PutObject, s3:GetObject)
4. Generar Access Key y Secret Key
5. Configurar las credenciales en `.env`

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

AWS_ACCESS_KEY_ID=tu_aws_access_key
AWS_SECRET_ACCESS_KEY=tu_aws_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET_NAME=tu-bucket-name

BACKUP_HOUR=2
BACKUP_MINUTE=0
```

### 4. Desplegar

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
│   ├── s3_uploader.py           # Módulo de AWS S3
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
- Verificar conectividad de red

### Error de autenticación en AWS S3
- Verificar que las credenciales AWS son correctas
- Verificar que el bucket existe y el usuario tiene permisos
- Verificar la región configurada

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
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [schedule](https://schedule.readthedocs.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
