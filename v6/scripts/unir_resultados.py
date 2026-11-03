#!/usr/bin/env python3
"""Une los JSON de varias ejecuciones parciales de run_tests_v63.py en uno solo (misma versión y entregables)."""
import json, sys
partes = [json.load(open(p)) for p in sys.argv[1:-1]]
base = dict(partes[0]); base["casos"] = []
for p in partes:
    assert p["entregables_probados"] == partes[0]["entregables_probados"], "los entregables probados no coinciden"
    base["casos"] += p["casos"]
base["total"] = len(base["casos"])
for k, v in (("superadas", "SUPERADA"), ("fallidas", "FALLIDA"), ("no_ejecutadas", "NO EJECUTADA")):
    base[k] = sum(c["resultado"] == v for c in base["casos"])
json.dump(base, open(sys.argv[-1], "w"), ensure_ascii=False, indent=1, default=str)
print(f"{base['superadas']} superadas · {base['fallidas']} fallidas · {base['no_ejecutadas']} no ejecutadas · total {base['total']} -> {sys.argv[-1]}")
