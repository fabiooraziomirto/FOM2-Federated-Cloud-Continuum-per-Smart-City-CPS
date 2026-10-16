"""Contratto di uscita: layout di una cartella di risultati per run.

experiments/results/<run-id>/
    metrics.csv       colonne: t_s, metric, value, tier
    provenance.json   chiavi: REQUIRED_PROVENANCE
    run.log
"""
from pathlib import Path
import json

REQUIRED_FILES = ("metrics.csv", "provenance.json", "run.log")
REQUIRED_PROVENANCE = ("descriptor_hash", "node_inventory", "impairment_log", "started_at")


def check_run_dir(path):
    """Ritorna la lista di problemi (vuota se la cartella rispetta il contratto)."""
    p = Path(path)
    errs = [f"manca {f}" for f in REQUIRED_FILES if not (p / f).is_file()]
    prov = p / "provenance.json"
    if prov.is_file():
        data = json.loads(prov.read_text())
        errs += [f"provenance: manca '{k}'" for k in REQUIRED_PROVENANCE if k not in data]
    return errs
