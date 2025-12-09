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
        Crea un backup de la base de datos PostgreSQL usando psycopg2
        Retorna la ruta del archivo de backup
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"backup_{self.db_name}_{timestamp}.sql"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            logger.info(f"Iniciando backup de la base de datos: {self.db_name}")
            
            # Conectar a la base de datos
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            
            # Abrir archivo para escribir el backup
            with open(backup_path, 'w') as f:
                # Escribir header del backup
                f.write(f"-- PostgreSQL database backup\n")
                f.write(f"-- Database: {self.db_name}\n")
                f.write(f"-- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                cursor = conn.cursor()
                
                # Obtener todas las tablas
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                """)
                tables = cursor.fetchall()
                
                logger.info(f"Encontradas {len(tables)} tablas para respaldar")
                
                # Para cada tabla, exportar su estructura y datos
                for table in tables:
                    table_name = table[0]
                    f.write(f"\n-- Table: {table_name}\n")
                    
                    # Obtener la estructura de la tabla (CREATE TABLE)
                    cursor.execute(f"""
                        SELECT 
                            'CREATE TABLE ' || quote_ident(table_name) || ' (' ||
                            string_agg(column_definition, ', ') || ');'
                        FROM (
                            SELECT 
                                table_name,
                                quote_ident(column_name) || ' ' || 
                                data_type ||
                                CASE 
                                    WHEN character_maximum_length IS NOT NULL 
                                    THEN '(' || character_maximum_length || ')'
                                    ELSE ''
                                END ||
                                CASE 
                                    WHEN is_nullable = 'NO' THEN ' NOT NULL'
                                    ELSE ''
                                END as column_definition
                            FROM information_schema.columns
                            WHERE table_name = '{table_name}'
                            ORDER BY ordinal_position
                        ) AS columns
                        GROUP BY table_name
                    """)
                    
                    create_table = cursor.fetchone()
                    if create_table:
                        f.write(f"DROP TABLE IF EXISTS {table_name} CASCADE;\n")
                        f.write(f"{create_table[0]}\n\n")
                    
                    # Obtener los datos de la tabla
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    
                    if rows:
                        # Obtener nombres de columnas
                        cursor.execute(f"""
                            SELECT column_name 
                            FROM information_schema.columns 
                            WHERE table_name = '{table_name}'
                            ORDER BY ordinal_position
                        """)
                        columns = [col[0] for col in cursor.fetchall()]
                        
                        f.write(f"-- Data for table: {table_name}\n")
                        for row in rows:
                            values = []
                            for val in row:
                                if val is None:
                                    values.append('NULL')
                                elif isinstance(val, str):
                                    # Escapar comillas simples
                                    val_escaped = val.replace("'", "''")
                                    values.append(f"'{val_escaped}'")
                                else:
                                    values.append(str(val))
                            
                            insert_stmt = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});\n"
                            f.write(insert_stmt)
                        f.write("\n")
                
                cursor.close()
                conn.close()
            
            logger.info(f"Backup creado exitosamente: {backup_path}")
            return backup_path
                
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
