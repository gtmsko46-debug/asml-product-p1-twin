# SPEC — asml-product-p1-twin (M1 champion module)

## Champion job

Given synthetic FEL/scanner coupling features, research pods **import** this
package and obtain IF metrics plus a documented uncertainty envelope:

| Metric | Meaning |
|--------|---------|
| `if_power_w` | Delivered intermediate-focus power (W) |
| `uniformity` | Illumination uniformity ∈ [0, 1] |
| `first_mirror_fluence` | First-mirror fluence under load |
| `illuminator_acceptance` | Illuminator acceptance of conditioned beam ∈ [0, 1] |

Assumption card: **`fel-scanner-twin-v1`**.

Public surface:

```python
from asml_product_p1_twin import simulate, TwinReport

report = simulate({
  "fel_power_kw": ..., "beam_split_ratio": ..., "undulator_k": ...,
  "scanner_na": ..., "pupil_fill": ..., "pulse_rep_hz": ...,
  "first_mirror_angle_deg": ...,
  # optional: "feeds": ["fel-01","fel-02","fel-03","fel-09"]
})
# report.if_power_w, .uniformity, .first_mirror_fluence, .illuminator_acceptance
# report.uncertainty  # per-metric σ (synthetic, documented)
# report.assumption_card_id == "fel-scanner-twin-v1"
# report.feeds_used
# report.to_dict()
```

Also: `predict_metrics(row) -> dict` — point estimates only.

## Sandbox contract

- Bench lab: `asml-bench/labs/p1-twin/`
- **Harness may edit only** `labs/p1-twin/twin.py`
- This product package is the **stable import surface**. Bundled
  `reference_twin.py` matches the SEED baseline so `pip install -e .` needs
  zero bench checkout.
- Live weights: set `ASML_BENCH_ROOT` (loads `labs/p1-twin/twin.py`) or
  `ASML_P1_TWIN_PATH` (path to a `twin.py`). Else → reference fallback.
- Never invoke lasercode from this PI. Hill-climbs go through Foreman stamps.

## Consumption map (feeds)

Default feeds consumed by the twin product:

| Feed | Role |
|------|------|
| FEL-01 | FEL source / power coupling |
| FEL-02 | Beam transport / split |
| FEL-03 | Undulator / pulse conditioning |
| FEL-09 | Scanner illuminator interface |

Override via `row["feeds"]` when a pod scopes a subset.

## Dual-island demo requirement

Research-facing demos require **dual-island**:

- STEM / twin solvers → `grok`
- Docs / scaffolding → `mistral` / `mistral-large-latest` via **lasercode-session**

(Do not call lasercode from this repository; Foreman owns session routing.)

## Factory milestones (asml-bench issues)

| M | Issue | Stage | Status |
|---|-------|-------|--------|
| Parent | [#4](https://github.com/gtmsko46-debug/asml-bench/issues/4) | backlog P0 | GO-LIVE |
| M0 | [#14](https://github.com/gtmsko46-debug/asml-bench/issues/14) | Lab freeze | **done** |
| M1 | [#15](https://github.com/gtmsko46-debug/asml-bench/issues/15) | Champion importable module | **this PR** |
| M2 | [#16](https://github.com/gtmsko46-debug/asml-bench/issues/16) | Dual SEED + KEEP climb | KEEP filed |
| M3 | [#17](https://github.com/gtmsko46-debug/asml-bench/issues/17) | KEEP → Repro → ship-queue | pending |

## SEED / KEEP notes (Experimentalist)

- **SEED landed:** HT-1007 (grok) + HT-1008 (mock-mistral) @
  `holdout_nrmse ≈ 0.6162` on the SEED baseline twin.
- **KEEP climb in flight:** HT-1013 (grok) + HT-1014 (mock-mistral).
  *(HT-1011/1012 are FEL-02 — not this product.)*

## Uncertainty model (synthetic)

`simulate` attaches per-metric σ from a **toy** model: relative floors scaled by
assumption-card confidence (`fel-scanner-twin-v1`). These are **not** fab
ground-truth; never invent confidential numbers. Marked synthetic in code and
docs so pods can distinguish envelope from point estimate.

## Package layout

```
asml_product_p1_twin/
  __init__.py          # simulate, TwinReport, ASSUMPTION_CARD, FEEDS_DEFAULT
  reference_twin.py    # bundled SEED-baseline physics twin
  loader.py            # ASML_BENCH_ROOT / ASML_P1_TWIN_PATH → live twin.py
  simulate.py          # TwinReport + uncertainty wrapper
```
