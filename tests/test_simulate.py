"""M1 contract tests for asml_product_p1_twin."""
from __future__ import annotations

import os
import unittest
from pathlib import Path
from unittest import mock

from asml_product_p1_twin import (
    ASSUMPTION_CARD,
    FEEDS_DEFAULT,
    TwinReport,
    predict_metrics,
    simulate,
)
from asml_product_p1_twin.loader import get_predict_twin, reset_loader_cache


SAMPLE = {
    "fel_power_kw": 12.0,
    "beam_split_ratio": 0.55,
    "undulator_k": 1.4,
    "scanner_na": 0.55,
    "pupil_fill": 0.75,
    "pulse_rep_hz": 100.0,
    "first_mirror_angle_deg": 8.0,
}


class TestSimulate(unittest.TestCase):
    def setUp(self) -> None:
        reset_loader_cache()
        os.environ.pop("ASML_BENCH_ROOT", None)
        os.environ.pop("ASML_P1_TWIN_PATH", None)

    def tearDown(self) -> None:
        reset_loader_cache()
        os.environ.pop("ASML_BENCH_ROOT", None)
        os.environ.pop("ASML_P1_TWIN_PATH", None)

    def test_report_keys_and_card(self) -> None:
        report = simulate(SAMPLE)
        self.assertIsInstance(report, TwinReport)
        self.assertEqual(report.assumption_card_id, "fel-scanner-twin-v1")
        self.assertEqual(report.assumption_card_id, ASSUMPTION_CARD)
        self.assertTrue(hasattr(report, "if_power_w"))
        self.assertTrue(hasattr(report, "uniformity"))
        self.assertTrue(hasattr(report, "first_mirror_fluence"))
        self.assertTrue(hasattr(report, "illuminator_acceptance"))
        d = report.to_dict()
        for key in (
            "if_power_w",
            "uniformity",
            "first_mirror_fluence",
            "illuminator_acceptance",
            "uncertainty",
            "assumption_card_id",
            "feeds_used",
        ):
            self.assertIn(key, d)

    def test_uncertainty_present(self) -> None:
        report = simulate(SAMPLE)
        self.assertIsInstance(report.uncertainty, dict)
        for metric in (
            "if_power_w",
            "uniformity",
            "first_mirror_fluence",
            "illuminator_acceptance",
        ):
            self.assertIn(metric, report.uncertainty)
            self.assertIsInstance(report.uncertainty[metric], float)
            self.assertGreater(report.uncertainty[metric], 0.0)

    def test_feeds_default(self) -> None:
        report = simulate(SAMPLE)
        self.assertEqual(list(report.feeds_used), list(FEEDS_DEFAULT))
        self.assertEqual(report.feeds_used, ["fel-01", "fel-02", "fel-03", "fel-09"])

    def test_feeds_override(self) -> None:
        row = {**SAMPLE, "feeds": ["fel-01"]}
        report = simulate(row)
        self.assertEqual(report.feeds_used, ["fel-01"])

    def test_loader_fallback_reference(self) -> None:
        source, fn = get_predict_twin(force_reload=True)
        self.assertEqual(source, "reference")
        out = fn(SAMPLE)
        self.assertIn("if_power_w", out)
        report = simulate(SAMPLE)
        self.assertEqual(report.twin_source, "reference")

    def test_loader_bench_path(self) -> None:
        # Prefer a real bench twin if present on this box; else write a stub.
        bench_twin = Path("/workspace/asml-bench/labs/p1-twin/twin.py")
        if bench_twin.is_file():
            with mock.patch.dict(os.environ, {"ASML_BENCH_ROOT": "/workspace/asml-bench"}):
                reset_loader_cache()
                source, fn = get_predict_twin(force_reload=True)
                self.assertTrue(source.endswith("twin.py"))
                out = fn(SAMPLE)
                self.assertIn("if_power_w", out)
        else:
            import tempfile

            with tempfile.TemporaryDirectory() as td:
                twin_path = Path(td) / "twin.py"
                twin_path.write_text(
                    "def predict_twin(row):\n"
                    "    return {k: 1.0 for k in ("
                    "'if_power_w','uniformity',"
                    "'first_mirror_fluence','illuminator_acceptance')}\n",
                    encoding="utf-8",
                )
                with mock.patch.dict(os.environ, {"ASML_P1_TWIN_PATH": str(twin_path)}):
                    reset_loader_cache()
                    source, fn = get_predict_twin(force_reload=True)
                    self.assertEqual(source, str(twin_path.resolve()))
                    self.assertEqual(fn(SAMPLE)["if_power_w"], 1.0)

    def test_predict_metrics_no_uncertainty(self) -> None:
        m = predict_metrics(SAMPLE)
        self.assertIn("if_power_w", m)
        self.assertNotIn("uncertainty", m)
        self.assertIsInstance(m["if_power_w"], float)


if __name__ == "__main__":
    unittest.main()
