import os
import json
import pickle
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class GoogleDriveUploader:
    def __init__(self):
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        self.folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        self.service = self._authenticate()
    
    def _authenticate(self):
        """
        Autentica con Google Drive usando credenciales de servicio o OAuth
        Soporta tanto archivo local como variable de entorno
        """
        try:
            # Primero intenta leer de variable GOOGLE_CREDENTIALS_FILE (para Railway)
            creds_json = os.getenv('GOOGLE_CREDENTIALS_FILE')
            if creds_json:
                try:
                    creds_dict = json.loads(creds_json)
                    creds = service_account.Credentials.from_service_account_info(
                        creds_dict,
                        scopes=['https://www.googleapis.com/auth/drive.file']
                    )
                    logger.info("Autenticación con Google Drive exitosa (desde GOOGLE_CREDENTIALS_FILE)")
                    return build('drive', 'v3', credentials=creds)
                except json.JSONDecodeError as e:
                    logger.error(f"Error al parsear JSON de GOOGLE_CREDENTIALS_FILE: {str(e)}")
                except Exception as e:
                    logger.error(f"Error al autenticar con GOOGLE_CREDENTIALS_FILE: {str(e)}")
            
            # Intenta GOOGLE_CREDENTIALS como alternativa
            creds_json = os.getenv('GOOGLE_CREDENTIALS')
            if creds_json:
                try:
                    creds_dict = json.loads(creds_json)
                    creds = service_account.Credentials.from_service_account_info(
                        creds_dict,
                        scopes=['https://www.googleapis.com/auth/drive.file']
                    )
                    logger.info("Autenticación con Google Drive exitosa (desde GOOGLE_CREDENTIALS)")
                    return build('drive', 'v3', credentials=creds)
                except json.JSONDecodeError as e:
                    logger.error(f"Error al parsear JSON de GOOGLE_CREDENTIALS: {str(e)}")
                except Exception as e:
                    logger.error(f"Error al autenticar con GOOGLE_CREDENTIALS: {str(e)}")
            
            # Si no hay variables de entorno, intenta usar archivo local
            credentials_file_path = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
            # Solo intenta leer como archivo si no es un JSON (es decir, es una ruta)
            if os.path.exists(credentials_file_path):
                creds = service_account.Credentials.from_service_account_file(
                    credentials_file_path,
                    scopes=['https://www.googleapis.com/auth/drive.file']
                )
                logger.info("Autenticación con Google Drive exitosa (desde archivo local)")
                return build('drive', 'v3', credentials=creds)
            else:
                logger.error("No se encontró credenciales de Google Drive")
                logger.error("Configura GOOGLE_CREDENTIALS_FILE con el JSON completo en Railway")
                return None
        except Exception as e:
            logger.error(f"Error en autenticación de Google Drive: {str(e)}")
            return None
    
    def upload_file(self, file_path, file_name=None):
        """
        Sube un archivo a Google Drive
        """
        try:
            if not self.service:
                logger.error("Servicio de Google Drive no disponible")
                return None
            
            if not os.path.exists(file_path):
                logger.error(f"Archivo no encontrado: {file_path}")
                return None
            
            if file_name is None:
                file_name = os.path.basename(file_path)
            
            # Crear metadatos del archivo
            file_metadata = {
                'name': file_name,
                'parents': [self.folder_id] if self.folder_id else []
            }
            
            # Crear el archivo en Google Drive
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            logger.info(f"Archivo subido a Google Drive: {file_name} (ID: {file['id']})")
            return file
            
        except Exception as e:
            logger.error(f"Error al subir archivo a Google Drive: {str(e)}")
            return None
    
    def list_files(self, limit=10):
        """
        Lista archivos en Google Drive
        """
        try:
            if not self.service:
                logger.error("Servicio de Google Drive no disponible")
                return []
            
            query = f"'{self.folder_id}' in parents" if self.folder_id else None
            results = self.service.files().list(
                spaces='drive',
                pageSize=limit,
                q=query,
                fields='files(id, name, createdTime)'
            ).execute()
            
            files = results.get('files', [])
            logger.info(f"Se encontraron {len(files)} archivos en Google Drive")
            return files
            
        except Exception as e:
            logger.error(f"Error al listar archivos: {str(e)}")
            return []
