# asml-product-p1-twin

**P0 product.** FEL↔scanner digital twin that research islands call.

## Champion job
Given synthetic FEL/scanner coupling features, report:
- `if_power_w`
- `uniformity`
- `first_mirror_fluence`
- `illuminator_acceptance`

## Bench
- Lab: `labs/p1-twin/` on [asml-bench](https://github.com/gtmsko46-debug/asml-bench)
- Sandbox (only editable under harness): `twin.py`
- Assumption card: `fel-scanner-twin-v1`
- Consumes: FEL-01 / FEL-02 / FEL-03 / FEL-09

## Factory milestones (asml-bench Issues)
| M | Issue | Stage |
|---|-------|-------|
| Parent | [#4](https://github.com/gtmsko46-debug/asml-bench/issues/4) | backlog P0 |
| M0 | [#14](https://github.com/gtmsko46-debug/asml-bench/issues/14) | Lab freeze |
| M1 | [#15](https://github.com/gtmsko46-debug/asml-bench/issues/15) | Spec / champion contract |
| M2 | [#16](https://github.com/gtmsko46-debug/asml-bench/issues/16) | Dual SEED (grok + mock-mistral) |
| M3 | [#17](https://github.com/gtmsko46-debug/asml-bench/issues/17) | KEEP → Repro → ship-queue |

## Provider
- STEM / twin solvers → `grok`
- Docs / scaffolding → `mock-mistral`
- Research-facing demos require **dual-island**

## Status
GO-LIVE. Hill-climbs only via Foreman stamped tickets. Never invoke lasercode from this PI.
