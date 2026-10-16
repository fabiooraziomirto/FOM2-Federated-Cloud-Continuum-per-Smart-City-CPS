# FOM2: Reproducible smart-city CPS experimentation over a federated cloud continuum

Full paper per i-Cities 2026 (Springer CCIS). Piano in `docs/piano-full-paper.md`.

| Cartella | Ruolo |
| --- | --- |
| `descriptor/` | Contratto d'ingresso: schema, validatore, esempio |
| `orchestrator/` | Thin layer: descriptor -> slices-cli, netem, K3s, SUMO, provenance |
| `workload/` | Applicazione CPS e scenario SUMO |
| `experiments/` | Descriptor per RQ e risultati grezzi (uno per run-id) |
| `analysis/` | Da risultati a grafici e tabelle |
| `paper/` | LaTeX (template llncs) |

Contratti: ingresso = descriptor YAML; uscita = `experiments/results/<run-id>/` (vedi `orchestrator/orchestrator/contract.py`).

`make validate`, `make test`, `make paper`.
