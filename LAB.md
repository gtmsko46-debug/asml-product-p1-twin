# asml-product-p1-twin

Owned by Twin PI + Product Manager on **gtmsko46-debug**.

- Shared bench + tickets: https://github.com/gtmsko46-debug/asml-bench
- Lab path: `labs/p1-twin/`
- Sandbox (harness-only): `twin.py`
- Product import: `pip install -e .` → `from asml_product_p1_twin import simulate`
- Harness: lasercode via **Foreman only** (never from this PI)
- Priority: **P0** (GO-LIVE)
- Queued behind this product: P2 coherence, P3 scheduler, P10 IF shim

## Live twin override

```bash
export ASML_BENCH_ROOT=/path/to/asml-bench   # → labs/p1-twin/twin.py
# or ASML_P1_TWIN_PATH=/path/to/twin.py
```

Unset → bundled `reference_twin` (SEED baseline). Mid-process env changes need
`get_predict_twin(force_reload=True)` or `reset_loader_cache()`.

## Provider tags

- STEM: `grok`
- Weak/scaffold: **`mock-mistral`** (champion lock stand-in
  `xai/grok-4.20-0309-non-reasoning`; do not stamp `mistral/*` for runs)

## Status

- [x] M0 lab freeze (#14)
- [x] M1 champion importable module (#15) — merged
- [x] Dual-gate KEEP candidate HT-1013/1014 (#30)
- [ ] KEEP → Repro → ship-queue (#17) — awaiting Repro

KEEP path: **#30 → #17** (not M2/#16). SEED HT-1007/1008 @ holdout_nrmse≈0.6162.
See [SPEC.md](./SPEC.md).
