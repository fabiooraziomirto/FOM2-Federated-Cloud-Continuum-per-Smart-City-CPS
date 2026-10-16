#!/usr/bin/env python3
"""Valida un experiment descriptor: schema JSON + controlli semantici."""
import json, sys, pathlib
import yaml
from jsonschema import Draft202012Validator

HERE = pathlib.Path(__file__).parent


def semantic_errors(d):
    err = []
    sites = d["infrastructure"]["sites"]
    ids = [s["id"] for s in sites]
    tiers = {s["tier"] for s in sites}
    if len(ids) != len(set(ids)):
        err.append("infrastructure.sites: id duplicati")
    for l in d["infrastructure"]["links"]:
        for end in (l["from"], l["to"]):
            if end not in ids:
                err.append(f"link {l['from']}->{l['to']}: sito '{end}' non definito")
    for s in sites:
        if s.get("provider", "slices-cli") == "slices-cli" and s["site"] == "local":
            err.append(f"site {s['id']}: 'local' richiede provider 'manual'")
        if s.get("provider") == "manual" and s["site"] != "local":
            err.append(f"site {s['id']}: provider 'manual' richiede site 'local'")
    profiles = {l["profile"] for l in d["infrastructure"]["links"]}
    for p in d["infrastructure"].get("impairments", {}):
        if p not in profiles:
            err.append(f"impairments.{p}: nessun link con questo profilo")
    comps = {c["name"] for c in d["application"]["components"]}
    for c in d["application"]["components"]:
        pl = c["placement"] if isinstance(c["placement"], list) else [c["placement"]]
        for t in pl:
            if t not in tiers:
                err.append(f"componente {c['name']}: tier '{t}' assente in infrastructure")
    for f in d["application"]["dataflows"]:
        for end in (f["from"], f["to"]):
            if end not in comps:
                err.append(f"dataflow {f['from']}->{f['to']}: componente '{end}' non definito")
    t = d["application"]["timing"]
    if t["deadline_ms"] > t["control_period_s"] * 1000:
        err.append("timing: deadline_ms supera control_period_s")
    ex = d["execution"]
    if ex["warmup_min"] >= ex["duration_min"]:
        err.append("execution: warmup_min >= duration_min")
    if d["observability"]["clock_sync"] == "none":
        err.append("observability: clock_sync 'none' non ammesso (R5)")
    # R6: una condizione non può essere sia controllata sia registrata
    controlled = set(d["infrastructure"].get("impairments", {}))
    for r in d["conditions"]["recorded"]:
        if r in controlled:
            err.append(f"conditions.recorded: '{r}' è anche controllata")
    return err


def main(path):
    d = yaml.safe_load(open(path))
    schema = json.load(open(HERE / "schema.json"))
    errs = [f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
            for e in Draft202012Validator(schema).iter_errors(d)]
    if not errs:
        errs = semantic_errors(d)
    for e in errs:
        print("ERRORE", e)
    print("OK" if not errs else f"{len(errs)} errori")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else HERE / "example.yaml"))
