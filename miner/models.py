from pydantic import BaseModel, Field
from typing import List, Optional

class Finding(BaseModel):
    rule_id: str
    severity: Optional[str] = None
    message: str
    file: str
    start_line: int

class Repository(BaseModel):
    name: str
    url: str
    status: str # Puede ser "analyzed", "failed_clone", "unsupported", etc.
    languages: List[str] = []
    findings: List[Finding] = []

class Summary(BaseModel):
    repositories: int = 0
    analyzed: int = 0
    failed: int = 0
    unsupported: int = 0
    findings: int = 0

class MinerOutput(BaseModel):
    organization: str
    summary: Summary
    repositories: List[Repository] = []
