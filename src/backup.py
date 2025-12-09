import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class PostgreSQLBackup:
    def __init__(self):
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
        
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self):
        """
        Crea un backup de la base de datos PostgreSQL
        Retorna la ruta del archivo de backup
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"backup_{self.db_name}_{timestamp}.sql"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Comando para pg_dump
            dump_command = f"PGPASSWORD={self.db_password} pg_dump -h {self.db_host} -p {self.db_port} -U {self.db_user} -d {self.db_name} -F p > {backup_path}"
            
            logger.info(f"Iniciando backup de la base de datos: {self.db_name}")
            result = os.system(dump_command)
            
            if result == 0:
                logger.info(f"Backup creado exitosamente: {backup_path}")
                return backup_path
            else:
                logger.error(f"Error al crear el backup. Código de error: {result}")
                return None
                
        except Exception as e:
            logger.error(f"Error en create_backup: {str(e)}")
            return None
    
    def verify_backup(self, backup_path):
        """
        Verifica que el archivo de backup existe y tiene contenido
        """
        try:
            if os.path.exists(backup_path) and os.path.getsize(backup_path) > 0:
                logger.info(f"Backup verificado: {backup_path}")
                return True
            else:
                logger.error(f"Backup inválido o vacío: {backup_path}")
                return False
        except Exception as e:
            logger.error(f"Error al verificar backup: {str(e)}")
            return False
