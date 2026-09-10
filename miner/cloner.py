import subprocess
import shutil
from pathlib import Path

def clone_repository(repo_url: str, repo_name: str, base_dir: Path) -> bool:
    """Clona un repositorio de GitHub. Retorna True si fue exitoso, False si falló."""
    repo_path = base_dir / repo_name
    
    # Si la carpeta ya existe de una prueba anterior, la eliminamos
    if repo_path.exists():
        shutil.rmtree(repo_path)
        
    try:
        # Ejecutamos el comando git clone de forma silenciosa
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(repo_path)],
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError:
        # Si falla (ej. repositorio vacío o sin permisos), capturamos el error
        return False
