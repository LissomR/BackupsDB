import os
import boto3
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class S3Uploader:
    def __init__(self):
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
        self.s3_client = self._authenticate()
    
    def _authenticate(self):
        """
        Autentica con AWS S3
        """
        try:
            if not self.aws_access_key or not self.aws_secret_key:
                logger.error("Faltan credenciales de AWS")
                return None
            
            if not self.bucket_name:
                logger.error("Falta el nombre del bucket S3")
                return None
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
            
            logger.info(f"Autenticación con AWS S3 exitosa (bucket: {self.bucket_name})")
            return s3_client
            
        except Exception as e:
            logger.error(f"Error en autenticación de AWS S3: {str(e)}")
            return None
    
    def upload_file(self, file_path, file_name=None):
        """
        Sube un archivo a S3
        """
        try:
            if not self.s3_client:
                logger.error("Cliente S3 no disponible")
                return None
            
            if not os.path.exists(file_path):
                logger.error(f"Archivo no encontrado: {file_path}")
                return None
            
            if file_name is None:
                file_name = os.path.basename(file_path)
            
            # Guardar en carpeta BackupsDB (la fecha ya está en el nombre del archivo)
            s3_key = f"BackupsDB/{file_name}"
            
            # Subir archivo
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            
            # Generar URL del archivo
            url = f"https://{self.bucket_name}.s3.{self.aws_region}.amazonaws.com/{s3_key}"
            
            logger.info(f"Archivo subido a S3: {s3_key}")
            logger.info(f"URL: {url}")
            
            return {
                'bucket': self.bucket_name,
                'key': s3_key,
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Error al subir archivo a S3: {str(e)}")
            return None
    
    def list_files(self, prefix='BackupsDB/', limit=10):
        """
        Lista archivos en S3
        """
        try:
            if not self.s3_client:
                logger.error("Cliente S3 no disponible")
                return []
            
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=limit
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified']
                    })
            
            logger.info(f"Se encontraron {len(files)} archivos en S3")
            return files
            
        except Exception as e:
            logger.error(f"Error al listar archivos: {str(e)}")
            return []
