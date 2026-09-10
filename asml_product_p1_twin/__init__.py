"""asml_product_p1_twin — champion-facing FEL↔scanner digital twin (M1).

Research pods import this package. Harness hill-climbs only touch
``asml-bench/labs/p1-twin/twin.py``; set ``ASML_BENCH_ROOT`` (or
``ASML_P1_TWIN_PATH``) to pick up live weights, else the bundled reference twin
is used.
"""

from .simulate import (
    ASSUMPTION_CARD,
    FEEDS_DEFAULT,
    TwinReport,
    predict_metrics,
    simulate,
)

__all__ = [
    "ASSUMPTION_CARD",
    "FEEDS_DEFAULT",
    "TwinReport",
    "predict_metrics",
    "simulate",
]

__version__ = "0.1.0"
