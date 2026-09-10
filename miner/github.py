import requests
from typing import List, Dict

def get_organization_repositories(org_name: str, token: str) -> List[Dict]:
    """Obtiene todos los repositorios de una organización usando la API de GitHub."""
    repos = []
    page = 1
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    while True:
        url = f"https://api.github.com/orgs/{org_name}/repos?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Error al consultar GitHub API: {response.text}")
            
        data = response.json()
        if not data:
            break # El ciclo se rompe cuando no hay más páginas
            
        repos.extend(data)
        page += 1
        
    return repos
