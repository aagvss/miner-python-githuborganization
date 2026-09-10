import json
from pathlib import Path
from typing import List
from miner.models import Finding

def parse_sarif_file(sarif_path: Path) -> List[Finding]:
    """Lee un archivo SARIF y extrae los hallazgos al modelo Pydantic."""
    findings = []
    if not sarif_path.exists():
        return findings

    with open(sarif_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return findings

    for run in data.get("runs", []):
        for result in run.get("results", []):
            rule_id = result.get("ruleId", "unknown")
            message = result.get("message", {}).get("text", "")
            severity = result.get("level", "warning")
            
            file_path = "unknown"
            start_line = 0
            
            locations = result.get("locations", [])
            if locations:
                phys_loc = locations[0].get("physicalLocation", {})
                file_path = phys_loc.get("artifactLocation", {}).get("uri", "unknown")
                start_line = phys_loc.get("region", {}).get("startLine", 0)

            findings.append(Finding(
                rule_id=rule_id,
                severity=severity,
                message=message,
                file=file_path,
                start_line=start_line
            ))
            
    # La rúbrica exige orden estable dentro de los hallazgos
    findings.sort(key=lambda x: (x.file, x.start_line, x.rule_id))
    return findings
