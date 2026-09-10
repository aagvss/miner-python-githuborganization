import os
import typer
import tempfile
from pathlib import Path

from miner.github import get_organization_repositories
from miner.cloner import clone_repository
from miner.codeql import run_codeql_analysis
from miner.parser import parse_sarif_file
from miner.models import MinerOutput, Summary, Repository, Finding

SUPPORTED_LANGUAGES = {"javascript": "javascript", "typescript": "javascript", "python": "python", "java": "java", "c": "cpp", "c++": "cpp", "c#": "csharp", "ruby": "ruby", "go": "go"}
app = typer.Typer()

@app.callback()
def callback(): pass

@app.command()
def scan(organization: str = typer.Option(..., "--organization"), output: Path = typer.Option(..., "--output")):
    token = os.environ.get("GITHUB_TOKEN")
    if not token: raise typer.Exit(code=1)

    repos_data = get_organization_repositories(organization, token)[:10] # Límite de 10
    
    # Inicializamos modelos Pydantic
    summary = Summary(repositories=len(repos_data))
    repositories_results = []

    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir)
        
        for repo in repos_data:
            repo_name = repo["name"]
            github_lang = repo.get("language")
            repo_model = Repository(name=repo_name, url=repo["clone_url"], status="pending")
            
            if github_lang: repo_model.languages.append(github_lang)
            
            if not github_lang or github_lang.lower() not in SUPPORTED_LANGUAGES:
                repo_model.status = "unsupported"
                summary.unsupported += 1
            elif not clone_repository(repo["clone_url"], repo_name, base_path):
                repo_model.status = "failed_clone"
                summary.failed += 1
            else:
                codeql_lang = SUPPORTED_LANGUAGES[github_lang.lower()]
                sarif_path = base_path / f"{repo_name}.sarif"
                
                if run_codeql_analysis(base_path / repo_name, base_path / f"{repo_name}-db", sarif_path, codeql_lang):
                    repo_model.status = "analyzed"
                    repo_model.findings = parse_sarif_file(sarif_path)
                    summary.analyzed += 1
                    summary.findings += len(repo_model.findings)
                else:
                    repo_model.status = "failed_analysis"
                    summary.failed += 1
            
            repositories_results.append(repo_model)

    # Ordenar repositorios alfabéticamente (Exigencia de la rúbrica)
    repositories_results.sort(key=lambda x: x.name)
    
    # Consolidar JSON
    final_output = MinerOutput(organization=organization, summary=summary, repositories=repositories_results)
    
    with open(output, "w", encoding="utf-8") as f:
        f.write(final_output.model_dump_json(indent=2))
        
    typer.secho(f"\n¡Éxito! Resultados reales guardados en: {output}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
