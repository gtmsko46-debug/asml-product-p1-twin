"""Bundled physics-shaped twin matching asml-bench labs/p1-twin/twin.py.

Synced from HT-1015 dual-KEEP (holdout 0.1489 / trap 0.2707).
Dual proof HT-1025 (0.2467/0.3356, IF=0.47 MIR=0.13).
HOLDOUT 2c398448a78b496b871794ad27d644d7a14b174426b538f1af7807f75bcc603c.
Critic+Repro+#17+Diplomat DUAL-KEEP; Lab Director #17 ship-queue APPROVED.

Ships with the package so ``pip install -e .`` works with zero bench checkout.
Harness hill-climbs only edit the bench sandbox; this copy is the frozen
fallback when ASML_BENCH_ROOT / ASML_P1_TWIN_PATH are unset.

Package API unchanged (``predict_twin`` used by loader/simulate).
"""
from __future__ import annotations

import math

# Non-zero coupling terms (guards void if ~0). Assumption-card bound.
IF_COUPLING = 0.55
MIRROR_LOAD = 0.12


def predict_twin(row: dict) -> dict:
    """Physics-structured map FEL/scanner features → IF metrics.

    Returns keys: if_power_w, uniformity, first_mirror_fluence, illuminator_acceptance.
    """
    fel_power_kw = float(row["fel_power_kw"])
    beam_split_ratio = float(row["beam_split_ratio"])
    undulator_k = float(row["undulator_k"])
    scanner_na = float(row["scanner_na"])
    pupil_fill = float(row["pupil_fill"])
    pulse_rep_hz = float(row["pulse_rep_hz"])
    first_mirror_angle_deg = float(row["first_mirror_angle_deg"])

    undulator_eff = (
        0.389
        + 0.166 * undulator_k
        + 0.112 * (undulator_k - 1.41) ** 2
        + 0.021 * math.sin(1.30 * undulator_k)
    )
    if_power_lin = (
        fel_power_kw * 1000.0 * beam_split_ratio * undulator_eff * IF_COUPLING
    )
    if_power_w = if_power_lin / (1.0 + if_power_lin / 12050.0)

    uniformity = (
        0.851
        + 0.121 * pupil_fill
        - 0.056 * abs(scanner_na - 0.55)
        + 0.026 * beam_split_ratio
        + 0.101 * pupil_fill * (scanner_na - 0.55)
        - 0.070 * (pupil_fill - 0.65) ** 2
    )
    uniformity = max(0.0, min(1.0, uniformity))

    angle_factor = (
        1.0
        + 0.0210 * first_mirror_angle_deg
        + 0.00246 * first_mirror_angle_deg ** 2
    )
    split_load = 1.0 + 0.088 * max(0.0, beam_split_ratio - 0.44) ** 2
    # Joint high-K / steep-graze / high-split load (empty train support)
    compound = (
        max(0.0, undulator_k - 2.35)
        * max(0.0, first_mirror_angle_deg - 23.0)
        * max(0.0, beam_split_ratio - 0.85)
    )
    first_mirror_fluence = (
        fel_power_kw
        * pulse_rep_hz
        * MIRROR_LOAD
        * angle_factor
        / max(scanner_na, 0.2)
        * split_load
        * (1.0 + 1.25 * compound)
    )

    illuminator_acceptance = (
        pupil_fill
        * beam_split_ratio
        * (0.699 + 0.230 * scanner_na)
        * (0.892 + 0.050 * math.tanh(undulator_k - 1.0))
        * (1.0 - 0.046 * abs(pupil_fill - 0.73))
        * (1.0 + 0.040 * math.tanh(scanner_na - 0.55))
    )
    illuminator_acceptance = max(0.0, min(1.0, illuminator_acceptance))

    return {
        "if_power_w": if_power_w,
        "uniformity": uniformity,
        "first_mirror_fluence": first_mirror_fluence,
        "illuminator_acceptance": illuminator_acceptance,
    }
