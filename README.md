# CodeQL Miner Automático

Herramienta CLI en Python para automatizar el análisis estático de vulnerabilidades en organizaciones de GitHub utilizando CodeQL.

## Instalación
1. Clonar este repositorio.
2. Crear y activar el entorno virtual: `python3 -m venv venv` y `source venv/bin/activate`.
3. Instalar dependencias: `pip install -e .`

## Configuración
Exportar el token de acceso personal de GitHub como variable de entorno (nunca incluirlo en el código):
`export GITHUB_TOKEN="tu_token_aqui"`

## Uso
Para ejecutar el análisis, utiliza el siguiente comando:
`miner scan --organization <nombre-org> --output resultados.json`
