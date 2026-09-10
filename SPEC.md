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
- If `ASML_BENCH_ROOT` / `ASML_P1_TWIN_PATH` change **mid-process**, call
  `get_predict_twin(force_reload=True)` (or `reset_loader_cache()`) — the
  loader caches the first resolved predictor.
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

## Provider / dual-island

Research-facing demos require **dual-island**. Prefer the **`mock-mistral`**
provider tag for the weak/scaffold lane (not `mistral/*` model IDs in run
stamps).

| Lane | Provider tag | Notes |
|------|--------------|-------|
| STEM / twin solvers | `grok` | Primary climb island |
| Docs / scaffold / weak island | `mock-mistral` | Champion lock stand-in model: `xai/grok-4.20-0309-non-reasoning` (Mistral-lane runs use this lock; do **not** stamp `mistral/*`) |

Foreman owns lasercode-session routing. Do not call lasercode from this repository.

## Factory milestones (asml-bench issues)

| M / path | Issue | Stage | Status |
|----------|-------|-------|--------|
| Parent | [#4](https://github.com/gtmsko46-debug/asml-bench/issues/4) | backlog P0 | GO-LIVE |
| M0 | [#14](https://github.com/gtmsko46-debug/asml-bench/issues/14) | Lab freeze | **done** |
| M1 | [#15](https://github.com/gtmsko46-debug/asml-bench/issues/15) | Champion importable module | **merged** |
| KEEP climb | [#30](https://github.com/gtmsko46-debug/asml-bench/issues/30) | Dual-gate KEEP (HT-1013/1014) | candidate filed |
| KEEP → ship | [#17](https://github.com/gtmsko46-debug/asml-bench/issues/17) | Repro → Critic → ship-queue | **awaiting Repro** |

KEEP path is **#30 → #17** (not M2/#16). M2 [#16](https://github.com/gtmsko46-debug/asml-bench/issues/16) was dual SEED and is closed.

## SEED / KEEP notes (Experimentalist)

- **SEED landed:** HT-1007 (grok) + HT-1008 (mock-mistral) @
  `holdout_nrmse ≈ 0.6162` on the SEED baseline twin.
- **Dual-gate KEEP candidate:** HT-1013 (grok) + HT-1014 (mock-mistral).
  Product `reference_twin` stays on SEED coeffs until Repro clean-tree
  confirms HT-1014. *(HT-1011/1012 are FEL-02 — not this product.)*

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
