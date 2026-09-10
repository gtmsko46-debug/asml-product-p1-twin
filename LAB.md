**SOFT (Critic):** HT-1027 dual proof is a thin IF_COUPLING-only retune vs HT-1025 (pred_diff PASS, not a comment fork). Explicit for promote hygiene.

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

Unset → bundled `reference_twin` (**HT-1026 dual-KEEP**). Mid-process env changes need
`get_predict_twin(force_reload=True)` or `reset_loader_cache()`.

## Provider tags

- STEM: `grok`
- Weak/scaffold: **`mock-mistral`** (champion lock stand-in
  `xai/grok-4.20-0309-non-reasoning`; do not stamp `mistral/*` for runs)

## Status

- [x] M0 lab freeze (#14)
- [x] M1 champion importable module (#15) — merged
- [x] **dual-KEEP landed** — `reference_twin` = **HT-1026** (holdout 0.1475 / trap 0.2534);
  dual proof **HT-1027** (0.1795/0.3076, IF=0.47 MIR=0.13);
  Critic+Repro+#17+Diplomat **DUAL-KEEP**; Lab Director **#17 ship-queue APPROVED**
- HOLDOUT digest `2c398448a78b496b871794ad27d644d7a14b174426b538f1af7807f75bcc603c`
- Deepen **HT-1026 / HT-1027** drafted (next climb)

**Ticket status:**

- **HT-1013: VOID** — oracle / `gen_fixtures.truth` coefficient clone; **not** product KEEP
- **HT-1014: Repro PASS** @ `holdout_nrmse=0.2554` — island/Repro-only; superseded by dual-KEEP
- **HT-1015 ∧ HT-1025: DUAL-KEEP** — product sync baseline; `reference_twin` = HT-1026 physics

KEEP path **#30 → #17** complete for this ship. See [SPEC.md](./SPEC.md).
