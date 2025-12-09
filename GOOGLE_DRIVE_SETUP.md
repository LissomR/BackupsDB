# Guía Paso a Paso: Configurar Google Drive para BackupsDB

## Paso 1: Crear un Proyecto en Google Cloud Console

### 1.1 Ir a Google Cloud Console
1. Ve a https://console.cloud.google.com/
2. Si no tienes cuenta de Google, crea una (gratis)
3. Inicia sesión

### 1.2 Crear un nuevo proyecto
1. En la parte superior, haz clic en el selector de proyectos (donde dice "My First Project" o similar)
2. Haz clic en "NEW PROJECT"
3. Dale un nombre: **BackupsDB** (o el que prefieras)
4. Haz clic en "CREATE"
5. Espera a que se cree el proyecto (puede tardar unos segundos)

## Paso 2: Activar la API de Google Drive

### 2.1 Buscar y activar la API
1. Una vez creado el proyecto, en el buscador superior escribe: **Google Drive API**
2. Haz clic en el resultado "Google Drive API"
3. Haz clic en el botón azul **"ENABLE"** (Activar)
4. Espera a que se active

## Paso 3: Crear una Cuenta de Servicio

### 3.1 Ir a la sección de Credenciales
1. En el menú izquierdo, busca **"Credentials"** (Credenciales)
2. Haz clic en **"Credentials"**

### 3.2 Crear una nueva credencial
1. En la parte superior, haz clic en **"+ CREATE CREDENTIALS"**
2. Selecciona **"Service Account"** (Cuenta de Servicio)

### 3.3 Completar el formulario
1. **Service account name**: Escribe **BackupsDB** (o un nombre descriptivo)
2. **Service account ID**: Se completa automáticamente
3. Haz clic en **"CREATE AND CONTINUE"**

### 3.4 Permisos (puedes dejar por defecto)
1. En la página de permisos, simplemente haz clic en **"CONTINUE"**

### 3.5 Crear la clave JSON
1. Haz clic en **"CREATE KEY"**
2. Selecciona **"JSON"**
3. Haz clic en **"CREATE"**
4. **Se descargará automáticamente** un archivo JSON

### 3.6 Guardar el archivo
1. Rename el archivo descargado a **`credentials.json`**
2. Guárdalo en la **raíz de tu proyecto** (en `/home/luis/BackupsDB/`)

## Paso 4: Crear una Carpeta en Google Drive

### 4.1 Ir a Google Drive
1. Ve a https://drive.google.com/
2. Inicia sesión con la **MISMA CUENTA** que usaste en Google Cloud Console

### 4.2 Crear una carpeta para los backups
1. Haz clic derecho en el espacio vacío
2. Selecciona **"Nueva carpeta"**
3. Dale el nombre: **BackupsDB** (o el que prefieras)
4. Presiona Enter

### 4.3 Obtener el ID de la carpeta
1. Abre la carpeta que acabas de crear
2. En la barra de direcciones, verás algo como:
   ```
   https://drive.google.com/drive/folders/AQUI_ESTA_EL_ID
   ```
3. Copia el ID (la parte larga de letras y números después de `/folders/`)

Ejemplo:
```
https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                       ESTE ES EL ID QUE NECESITAS
```

## Paso 5: Compartir la Carpeta con la Cuenta de Servicio

### 5.1 Obtener el email de la cuenta de servicio
1. Ve de nuevo a Google Cloud Console
2. Ve a **Credentials** (Credenciales)
3. En la sección "Service Accounts", haz clic en la cuenta que creaste
4. En la pestaña **"Details"**, busca **"Email"**
5. Copia el email (algo como: `backupsdb@...iam.gserviceaccount.com`)

### 5.2 Compartir la carpeta
1. Ve a Google Drive
2. Haz clic derecho en la carpeta **BackupsDB**
3. Selecciona **"Compartir"**
4. En el campo de texto, pega el email de la cuenta de servicio
5. Dale permisos de **"Editor"**
6. Desmarca **"Notificar a las personas"**
7. Haz clic en **"Compartir"**

## Paso 6: Configurar tu aplicación

### 6.1 Configurar el archivo `.env`
1. En tu carpeta del proyecto `/home/luis/BackupsDB/`, abre o crea el archivo `.env`
2. Completa las variables (puedes copiar de `.env.example`):

```bash
# PostgreSQL Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_contraseña_postgres

# Google Drive Configuration
GOOGLE_DRIVE_FOLDER_ID=AQUI_PEGA_EL_ID_DE_LA_CARPETA
GOOGLE_CREDENTIALS_FILE=credentials.json

# Schedule Configuration (backup cada día a las 2:00 AM)
BACKUP_HOUR=2
BACKUP_MINUTE=0
```

### 6.2 Ejemplo completo
```bash
# PostgreSQL Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mi_base_datos
DB_USER=postgres
DB_PASSWORD=mi_contraseña123

# Google Drive Configuration
GOOGLE_DRIVE_FOLDER_ID=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
GOOGLE_CREDENTIALS_FILE=credentials.json

# Schedule Configuration
BACKUP_HOUR=2
BACKUP_MINUTE=0
```

## Paso 7: Verificar que todo funciona

### 7.1 Desde tu computadora (local)
```bash
cd /home/luis/BackupsDB
source venv/bin/activate
python src/scheduler.py
```

### 7.2 Ver los logs
```bash
tail -f logs/backup_$(date +%Y%m%d).log
```

## Resumen de Archivos Necesarios

Después de completar todos los pasos, debes tener:

```
/home/luis/BackupsDB/
├── .env                          ← ARCHIVO IMPORTANTE (NO COMPARTIR)
│   Contiene credenciales de PostgreSQL
│
├── credentials.json              ← ARCHIVO IMPORTANTE (NO COMPARTIR)
│   Descargado de Google Cloud Console
│
├── src/
│   ├── backup.py
│   ├── google_drive.py
│   └── scheduler.py
│
└── README.md
```

## Checklist de Verificación ✓

- [ ] Creé un proyecto en Google Cloud Console
- [ ] Activé la Google Drive API
- [ ] Creé una cuenta de servicio
- [ ] Descargué el archivo `credentials.json`
- [ ] Guardé `credentials.json` en `/home/luis/BackupsDB/`
- [ ] Creé una carpeta en Google Drive llamada "BackupsDB"
- [ ] Copié el ID de la carpeta
- [ ] Compartí la carpeta con la cuenta de servicio
- [ ] Configuré el archivo `.env` con mis credenciales
- [ ] Probé la aplicación ejecutando `python src/scheduler.py`

## Troubleshooting (Si algo no funciona)

### Error: "File not found: credentials.json"
- Verifica que el archivo `credentials.json` está en `/home/luis/BackupsDB/`
- El archivo debe estar en la **raíz del proyecto**, no en una subcarpeta

### Error: "Permission denied" en Google Drive
- Verifica que compartiste la carpeta con el email de la cuenta de servicio
- Verifica que le diste permisos de "Editor"

### Error: "Invalid folder ID"
- Copia nuevamente el ID desde la barra de direcciones
- Asegúrate de no incluir caracteres adicionales

### El backup no se sube a Google Drive
- Revisa los logs: `tail -f logs/backup_*.log`
- Verifica que la carpeta en Google Drive existe y tiene el ID correcto

## Seguridad - IMPORTANTE ⚠️

- **NUNCA** compartas tu archivo `.env` en GitHub
- **NUNCA** compartas tu archivo `credentials.json` en GitHub
- Ambos archivos están en `.gitignore` por seguridad
- Protege tus credenciales como si fuesen contraseñas

---

¿Necesitas ayuda en algún paso específico? Dime cuál es el número del paso donde te atascas.
