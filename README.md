# asml-product-p1-twin

**P0 product.** FEL↔scanner digital twin that research islands actually import —
not a lab-only sandbox. M1 ships the installable module `asml_product_p1_twin`.

## Install

```bash
git clone https://github.com/gtmsko46-debug/asml-product-p1-twin
cd asml-product-p1-twin
pip install -e .
# or with tests: pip install -e '.[dev]'
```

Zero bench checkout required. Bundled `reference_twin` matches the asml-bench
`labs/p1-twin/twin.py` SEED baseline. To pick up live hill-climbed weights:

```bash
export ASML_BENCH_ROOT=/path/to/asml-bench
# or: export ASML_P1_TWIN_PATH=/path/to/labs/p1-twin/twin.py
```

If those env vars change **mid-process**, reload explicitly:

```python
from asml_product_p1_twin.loader import get_predict_twin, reset_loader_cache

reset_loader_cache()
# or: get_predict_twin(force_reload=True)
```

Harness edits **only** bench `twin.py`. This package is the stable import surface.

## Import (champion API)

```python
from asml_product_p1_twin import simulate, TwinReport

report = simulate({
    "fel_power_kw": 12.0,
    "beam_split_ratio": 0.55,
    "undulator_k": 1.4,
    "scanner_na": 0.55,
    "pupil_fill": 0.75,
    "pulse_rep_hz": 100.0,
    "first_mirror_angle_deg": 8.0,
    # optional: "feeds": ["fel-01", "fel-02", "fel-03", "fel-09"]
})

print(report.if_power_w, report.uniformity,
      report.first_mirror_fluence, report.illuminator_acceptance)
print(report.uncertainty)            # per-metric σ (synthetic, documented)
assert report.assumption_card_id == "fel-scanner-twin-v1"
print(report.feeds_used)
print(report.to_dict())
```

Point estimates only: `from asml_product_p1_twin import predict_metrics`.

Smoke: `python examples/smoke_import.py`

## Champion job

Synthetic FEL/scanner coupling → IF metrics under assumption card
`fel-scanner-twin-v1`. Consumes feeds **FEL-01 / FEL-02 / FEL-03 / FEL-09**.

Uncertainty is a documented toy envelope (card confidence + metric floors) —
**synthetic**, not confidential fab data.

## Bench / sandbox

| | |
|--|--|
| Lab | `labs/p1-twin/` on [asml-bench](https://github.com/gtmsko46-debug/asml-bench) |
| Sandbox (harness-only) | `twin.py` |
| Assumption card | `fel-scanner-twin-v1` |
| Spec | [SPEC.md](./SPEC.md) |

## Factory milestones

| M / path | Issue | Stage | Status |
|----------|-------|-------|--------|
| Parent | [#4](https://github.com/gtmsko46-debug/asml-bench/issues/4) | backlog P0 | GO-LIVE |
| M0 | [#14](https://github.com/gtmsko46-debug/asml-bench/issues/14) | Lab freeze | [x] done |
| M1 | [#15](https://github.com/gtmsko46-debug/asml-bench/issues/15) | Champion importable module | [x] **merged** |
| KEEP climb | [#30](https://github.com/gtmsko46-debug/asml-bench/issues/30) | Dual-gate KEEP (HT-1013/1014) | [x] candidate |
| KEEP → ship | [#17](https://github.com/gtmsko46-debug/asml-bench/issues/17) | Repro → Critic → ship-queue | [ ] **awaiting Repro** |

KEEP path is **#30 → #17** (not M2/#16). M2 [#16](https://github.com/gtmsko46-debug/asml-bench/issues/16) (dual SEED) is closed.

### SEED / KEEP

- SEED: HT-1007 / HT-1008 @ `holdout_nrmse ≈ 0.6162`
- Dual-gate KEEP candidate: HT-1013 (grok) + HT-1014 (mock-mistral)
  — not HT-1011/1012 (those are FEL-02)
- Bundled `reference_twin` remains SEED coeffs until Repro clean-tree confirms HT-1014

## Provider / dual-island

Prefer the **`mock-mistral`** provider tag for the weak/scaffold lane.

| Lane | Provider tag | Notes |
|------|--------------|-------|
| STEM / twin solvers | `grok` | Primary climb island |
| Docs / scaffold / weak island | `mock-mistral` | Champion lock stand-in: `xai/grok-4.20-0309-non-reasoning` (do **not** stamp `mistral/*` for runs) |

Research-facing demos require **dual-island**. Never invoke lasercode from this PI; Foreman owns harness stamps.

## Status

- [x] M0 lab freeze (#14)
- [x] M1 champion importable module (#15) — merged
- [x] Dual-gate KEEP candidate HT-1013/1014 (#30)
- [ ] KEEP → Repro → ship-queue (#17) — awaiting Repro

GO-LIVE. Hill-climbs only via Foreman stamped tickets.
