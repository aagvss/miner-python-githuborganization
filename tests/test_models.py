from miner.models import Finding, Summary

def test_finding_model_defaults():
    # Verifica que Pydantic asigne correctamente los valores y maneje los opcionales
    finding = Finding(rule_id="xss-rule", message="Error XSS", file="app.py", start_line=15)
    assert finding.rule_id == "xss-rule"
    assert finding.severity is None # El valor por defecto esperado

def test_summary_accumulation():
    # Verifica que el resumen guarde los conteos correctos
    summary = Summary(repositories=10, analyzed=0, failed=2, unsupported=8, findings=0)
    assert summary.repositories == 10
    assert summary.unsupported == 8
