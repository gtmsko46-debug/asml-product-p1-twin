#!/usr/bin/env python3
"""One-liner researchers can copy — champion import surface smoke."""
from asml_product_p1_twin import simulate

report = simulate(
    {
        "fel_power_kw": 12.0,
        "beam_split_ratio": 0.55,
        "undulator_k": 1.4,
        "scanner_na": 0.55,
        "pupil_fill": 0.75,
        "pulse_rep_hz": 100.0,
        "first_mirror_angle_deg": 8.0,
        # optional: "feeds": ["fel-01", "fel-02", "fel-03", "fel-09"],
    }
)
print(report.to_dict())
