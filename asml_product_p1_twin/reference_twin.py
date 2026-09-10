"""Bundled physics-shaped twin matching asml-bench labs/p1-twin/twin.py baseline.

Ships with the package so ``pip install -e .`` works with zero bench checkout.
Harness hill-climbs only edit the bench sandbox; this copy is the frozen
fallback when ASML_BENCH_ROOT / ASML_P1_TWIN_PATH are unset.
"""
from __future__ import annotations

import math

# Non-zero coupling terms (guards void if ~0). Intentionally weak vs fixture truth.
# Synced from asml-bench labs/p1-twin/twin.py SEED baseline (HT-1007/1008).
IF_COUPLING = 0.42  # should be learned toward ~0.55
MIRROR_LOAD = 0.09  # should be learned toward ~0.12


def predict_twin(row: dict) -> dict:
    """Physics-ish linear toy: map FEL/scanner features → IF metrics.

    Returns keys: if_power_w, uniformity, first_mirror_fluence, illuminator_acceptance.
    """
    fel_power_kw = float(row["fel_power_kw"])
    beam_split_ratio = float(row["beam_split_ratio"])
    undulator_k = float(row["undulator_k"])
    scanner_na = float(row["scanner_na"])
    pupil_fill = float(row["pupil_fill"])
    pulse_rep_hz = float(row["pulse_rep_hz"])
    first_mirror_angle_deg = float(row["first_mirror_angle_deg"])

    # Delivered IF power: FEL × split × undulator efficiency × IF coupling
    undulator_eff = 0.38 + 0.12 * undulator_k
    if_power_w = (
        fel_power_kw * 1000.0 * beam_split_ratio * undulator_eff * IF_COUPLING
    )

    # Illumination uniformity: pupil fill helps; NA mismatch hurts (toy)
    uniformity = (
        0.82
        + 0.10 * pupil_fill
        - 0.04 * abs(scanner_na - 0.55)
        + 0.02 * beam_split_ratio
    )
    uniformity = max(0.0, min(1.0, uniformity))

    # First-mirror fluence under load (angle softens footprint slightly)
    angle_factor = 1.0 + 0.015 * first_mirror_angle_deg
    first_mirror_fluence = (
        fel_power_kw * pulse_rep_hz * MIRROR_LOAD * angle_factor / max(scanner_na, 0.2)
    )

    # Illuminator acceptance of the conditioned beam
    illuminator_acceptance = (
        pupil_fill
        * beam_split_ratio
        * (0.65 + 0.18 * scanner_na)
        * (0.9 + 0.05 * math.tanh(undulator_k - 1.0))
    )
    illuminator_acceptance = max(0.0, min(1.0, illuminator_acceptance))

    return {
        "if_power_w": if_power_w,
        "uniformity": uniformity,
        "first_mirror_fluence": first_mirror_fluence,
        "illuminator_acceptance": illuminator_acceptance,
    }
