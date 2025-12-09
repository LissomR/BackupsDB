import schedule
import time
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

from backup import PostgreSQLBackup
from google_drive import GoogleDriveUploader

# Configurar logging
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"backup_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

load_dotenv()

class BackupScheduler:
    def __init__(self):
        self.backup = PostgreSQLBackup()
        self.drive = GoogleDriveUploader()
        self.backup_hour = str(os.getenv('BACKUP_HOUR', '2')).zfill(2)
        self.backup_minute = str(os.getenv('BACKUP_MINUTE', '0')).zfill(2)
    
    def perform_backup(self):
        """
        Ejecuta el proceso completo de backup:
        1. Crea el backup de PostgreSQL
        2. Sube a Google Drive
        """
        try:
            logger.info("=" * 60)
            logger.info("Iniciando proceso de backup automático")
            logger.info("=" * 60)
            
            # Paso 1: Crear backup
            backup_path = self.backup.create_backup()
            if not backup_path:
                logger.error("No se pudo crear el backup")
                return False
            
            # Paso 2: Verificar backup
            if not self.backup.verify_backup(backup_path):
                logger.error("El backup no pasó la verificación")
                return False
            
            # Paso 3: Subir a Google Drive
            logger.info("Subiendo backup a Google Drive...")
            if self.drive.upload_file(backup_path):
                logger.info("Backup subido a Google Drive exitosamente")
            else:
                logger.warning("No se pudo subir a Google Drive (continuando...)")
            
            logger.info("=" * 60)
            logger.info("Proceso de backup completado")
            logger.info("=" * 60)
            return True
            
        except Exception as e:
            logger.error(f"Error en perform_backup: {str(e)}")
            return False
    
    def schedule_backups(self):
        """
        Configura el programador de tareas
        """
        try:
            schedule_time = f"{self.backup_hour}:{self.backup_minute}"
            logger.info(f"Programando backup diario a las {schedule_time}")
            schedule.every().day.at(schedule_time).do(self.perform_backup)
            logger.info(f"Backup programado exitosamente para las {schedule_time}")
        except Exception as e:
            logger.error(f"Error al programar backup: {str(e)}")
            logger.error(f"BACKUP_HOUR={self.backup_hour}, BACKUP_MINUTE={self.backup_minute}")
            raise
    
    def start(self):
        """
        Inicia el scheduler
        """
        try:
            logger.info("Iniciando scheduler de backups")
            self.schedule_backups()
            
            # Loop principal
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verificar cada minuto
        except KeyboardInterrupt:
            logger.info("Scheduler detenido por el usuario")
        except Exception as e:
            logger.error(f"Error en el scheduler: {str(e)}")

if __name__ == "__main__":
    scheduler = BackupScheduler()
    scheduler.start()
