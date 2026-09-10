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

Unset → bundled `reference_twin` (SEED baseline).

## Status

- [x] M0 lab freeze (#14)
- [x] M1 champion importable module (#15)
- [ ] M2 KEEP climb HT-1013 (grok) + HT-1014 (mock-mistral); dual SEED (#16)
- [ ] M3 KEEP / ship (#17)

SEED HT-1007/1008 @ holdout_nrmse≈0.6162. See [SPEC.md](./SPEC.md).
