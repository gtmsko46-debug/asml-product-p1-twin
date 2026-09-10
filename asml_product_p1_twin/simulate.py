"""Champion-facing simulate API: metrics + synthetic uncertainty.

Uncertainty is a **toy / documented** model — relative σ derived from
assumption-card confidence plus fixed floors per metric. Numbers are synthetic;
they are not confidential fab data and must not be treated as such.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping, Sequence

from .loader import get_predict_twin

ASSUMPTION_CARD = "fel-scanner-twin-v1"
FEEDS_DEFAULT: tuple[str, ...] = ("fel-01", "fel-02", "fel-03", "fel-09")

# Synthetic uncertainty model (documented, not fab-grounded).
# Card confidence scales relative σ; floors prevent zero-width bands on small metrics.
_CARD_CONFIDENCE = 0.72  # fel-scanner-twin-v1 SEED-era confidence (synthetic)
_REL_SIGMA = {
    "if_power_w": 0.08,
    "uniformity": 0.03,
    "first_mirror_fluence": 0.10,
    "illuminator_acceptance": 0.04,
}
_FLOOR_SIGMA = {
    "if_power_w": 1.0,
    "uniformity": 0.005,
    "first_mirror_fluence": 0.5,
    "illuminator_acceptance": 0.005,
}

_REQUIRED_KEYS = (
    "fel_power_kw",
    "beam_split_ratio",
    "undulator_k",
    "scanner_na",
    "pupil_fill",
    "pulse_rep_hz",
    "first_mirror_angle_deg",
)


@dataclass
class TwinReport:
    """Product report returned by :func:`simulate`."""

    if_power_w: float
    uniformity: float
    first_mirror_fluence: float
    illuminator_acceptance: float
    uncertainty: dict[str, float]
    assumption_card_id: str = ASSUMPTION_CARD
    feeds_used: list[str] = field(default_factory=lambda: list(FEEDS_DEFAULT))
    twin_source: str = "reference"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _uncertainty_for(metrics: Mapping[str, float]) -> dict[str, float]:
    """Toy σ: max(floor, |value| * rel * (1.25 - confidence)). Synthetic."""
    scale = 1.25 - _CARD_CONFIDENCE
    out: dict[str, float] = {}
    for key, value in metrics.items():
        rel = _REL_SIGMA.get(key, 0.05)
        floor = _FLOOR_SIGMA.get(key, 1e-3)
        out[key] = float(max(floor, abs(float(value)) * rel * scale))
    return out


def predict_metrics(row: Mapping[str, Any]) -> dict[str, float]:
    """Thin wrapper: point estimates only (no uncertainty envelope)."""
    payload = {k: row[k] for k in _REQUIRED_KEYS}
    _source, predict = get_predict_twin()
    raw = predict(payload)
    return {k: float(raw[k]) for k in _REL_SIGMA}


def simulate(row: Mapping[str, Any]) -> TwinReport:
    """Run the twin and attach synthetic per-metric uncertainty.

    Optional ``row["feeds"]`` overrides the default FEL feed list.
    """
    feeds: Sequence[str]
    if "feeds" in row and row["feeds"] is not None:
        feeds = list(row["feeds"])
    else:
        feeds = list(FEEDS_DEFAULT)

    payload = {k: row[k] for k in _REQUIRED_KEYS}
    source, predict = get_predict_twin()
    raw = predict(payload)
    metrics = {k: float(raw[k]) for k in _REL_SIGMA}
    return TwinReport(
        if_power_w=metrics["if_power_w"],
        uniformity=metrics["uniformity"],
        first_mirror_fluence=metrics["first_mirror_fluence"],
        illuminator_acceptance=metrics["illuminator_acceptance"],
        uncertainty=_uncertainty_for(metrics),
        assumption_card_id=ASSUMPTION_CARD,
        feeds_used=list(feeds),
        twin_source=source,
    )
