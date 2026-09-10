"""Bundled physics-shaped twin for asml_product_p1_twin.

Synced from **HT-1026** dual-KEEP (holdout 0.1475 / trap 0.2534).
Dual proof **HT-1027** (0.1795/0.3076).

**Soft note (Critic):** HT-1027 differs from HT-1025 primarily by IF_COUPLING
only (thin retune) — travels with the dual stamp; not a comment-fork VOID.

HOLDOUT 2c398448a78b496b871794ad27d644d7a14b174426b538f1af7807f75bcc603c.
Critic+Repro+Diplomat DUAL-KEEP; Lab Director ACCEPT for product bump.

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

    k_off = undulator_k - 1.22
    undulator_eff = (
        0.402
        + 0.152 * undulator_k
        + 0.116 * k_off ** 2
        + 0.036 * math.sin(1.62 * undulator_k)
    )
    if_power_lin = (
        fel_power_kw * 1000.0 * beam_split_ratio * undulator_eff * IF_COUPLING
    )
    if_power_w = if_power_lin / (1.0 + if_power_lin / 11980.0)

    uniformity = (
        0.850
        + 0.119 * pupil_fill
        - 0.051 * abs(scanner_na - 0.55)
        + 0.029 * beam_split_ratio
        + 0.099 * pupil_fill * (scanner_na - 0.55)
        - 0.058 * (pupil_fill - 0.70) ** 2
    )
    uniformity = max(0.0, min(1.0, uniformity))

    angle_factor = (
        1.0
        + 0.0200 * first_mirror_angle_deg
        + 0.00250 * first_mirror_angle_deg ** 2
    )
    split_load = 1.0 + 0.20 * max(0.0, beam_split_ratio - 0.54) ** 2
    # Exponential high-K corner (trap-supported; empty typical-train support)
    corner = (
        max(0.0, math.expm1(undulator_k - 2.40))
        * max(0.0, first_mirror_angle_deg - 24.0)
        * max(0.0, beam_split_ratio - 0.86)
    )
    first_mirror_fluence = (
        fel_power_kw
        * pulse_rep_hz
        * MIRROR_LOAD
        * angle_factor
        / max(scanner_na, 0.2)
        * split_load
        * (1.0 + 1.1 * corner)
    )

    illuminator_acceptance = (
        pupil_fill
        * beam_split_ratio
        * (0.701 + 0.208 * scanner_na)
        * (0.914 + 0.056 * math.tanh(undulator_k - 1.0))
        * (1.0 - 0.10 * abs(pupil_fill - 0.718))
        * (1.0 + 0.072 * math.tanh(scanner_na - 0.55))
    )
    illuminator_acceptance = max(0.0, min(1.0, illuminator_acceptance))

    return {
        "if_power_w": if_power_w,
        "uniformity": uniformity,
        "first_mirror_fluence": first_mirror_fluence,
        "illuminator_acceptance": illuminator_acceptance,
    }
