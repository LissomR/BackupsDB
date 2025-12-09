import os
from github import Github
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class GitHubUploader:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.repo_owner = os.getenv('GITHUB_REPO_OWNER')
        self.repo_name = os.getenv('GITHUB_REPO_NAME')
        self.github = Github(self.token)
        self.repo = self._get_repo()
    
    def _get_repo(self):
        """
        Obtiene la referencia del repositorio
        """
        try:
            repo = self.github.get_user(self.repo_owner).get_repo(self.repo_name)
            logger.info(f"Repositorio conectado: {self.repo_owner}/{self.repo_name}")
            return repo
        except Exception as e:
            logger.error(f"Error al conectar con el repositorio: {str(e)}")
            return None
    
    def upload_file(self, file_path, commit_message=None, branch='main'):
        """
        Sube un archivo al repositorio GitHub
        """
        try:
            if not self.repo:
                logger.error("Repositorio no disponible")
                return None
            
            if not os.path.exists(file_path):
                logger.error(f"Archivo no encontrado: {file_path}")
                return None
            
            file_name = os.path.basename(file_path)
            
            # Leer el contenido del archivo
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Crear el mensaje de commit
            if commit_message is None:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                commit_message = f"Backup automático: {file_name} ({timestamp})"
            
            try:
                # Intentar obtener el archivo si ya existe
                existing_file = self.repo.get_contents(file_name, ref=branch)
                # Si existe, actualizar
                self.repo.update_file(
                    file_name,
                    commit_message,
                    content,
                    existing_file.sha,
                    branch=branch
                )
                logger.info(f"Archivo actualizado en GitHub: {file_name}")
            except:
                # Si no existe, crear
                self.repo.create_file(
                    file_name,
                    commit_message,
                    content,
                    branch=branch
                )
                logger.info(f"Archivo creado en GitHub: {file_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error al subir archivo a GitHub: {str(e)}")
            return False
    
    def create_backup_folder(self, folder_name='backups'):
        """
        Crea una carpeta de backups en el repositorio
        """
        try:
            if not self.repo:
                logger.error("Repositorio no disponible")
                return False
            
            # Crear un archivo README en la carpeta de backups
            readme_path = f"{folder_name}/README.md"
            readme_content = "# Backups Automáticos\n\nEsta carpeta contiene backups automáticos de la base de datos."
            
            try:
                self.repo.get_contents(readme_path)
            except:
                self.repo.create_file(
                    readme_path,
                    f"Crear carpeta {folder_name}",
                    readme_content
                )
                logger.info(f"Carpeta de backups creada en GitHub: {folder_name}")
            
            return True
        except Exception as e:
            logger.error(f"Error al crear carpeta en GitHub: {str(e)}")
            return False
