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
- [ ] Honest dual-gate KEEP → Repro → ship-queue (#17) — **still waiting**
  (HT-1015/1016 path after new HOLDOUT; fixture harden v2 digest `2c398448a78b496b871794ad27d644d7a14b174426b538f1af7807f75bcc603c` (HT-1018 / asml-bench PR #34))

**Ticket status (not product KEEP):**

- **HT-1013: VOID** — oracle / `gen_fixtures.truth` coefficient clone; **not** product KEEP
- **HT-1014: Repro PASS** @ `holdout_nrmse=0.2554` — island/Repro-only; **NOT** #17,
  **NOT** product dual-gate KEEP, **NOT** `reference_twin` sync baseline
- **`reference_twin`:** untouched / weights frozen until honest dual-gate KEEP + Repro

KEEP path remains **#30 → #17** (not M2/#16). SEED HT-1007/1008 @ holdout_nrmse≈0.6162.
See [SPEC.md](./SPEC.md).
