import subprocess
from pathlib import Path

def run_codeql_analysis(repo_dir: Path, db_dir: Path, sarif_output: Path, language: str = "javascript") -> bool:
    """
    Automatiza la creación de la base de datos de CodeQL y su análisis.
    Retorna True si ambos procesos fueron exitosos, False en caso contrario.
    """
    try:
        # 1. Comando para crear la base de datos
        subprocess.run(
            ["codeql", "database", "create", str(db_dir), f"--language={language}", f"--source-root={repo_dir}"],
            check=True,
            capture_output=True
        )
        
        # 2. Comando para analizar la base de datos y generar el SARIF
        subprocess.run(
            ["codeql", "database", "analyze", str(db_dir), "--format=sarif-latest", f"--output={sarif_output}", "--threads=0"],
            check=True,
            capture_output=True
        )
        return True
        
    except subprocess.CalledProcessError as e:
        # Si CodeQL falla (ej. lenguaje incorrecto o error de sintaxis en el repo)
        return False
