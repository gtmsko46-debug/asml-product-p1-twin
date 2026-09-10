"""Resolve which twin implementation to call.

Harness edits **only** ``asml-bench/labs/p1-twin/twin.py``. This product package
is the stable import surface researchers use. Live hill-climbed weights are
picked up when an env var points at that sandbox; otherwise the bundled
``reference_twin`` (SEED baseline) is used.

Env (first match wins):
  ASML_P1_TWIN_PATH  — path to a twin.py file, or a directory containing twin.py
  ASML_BENCH_ROOT    — asml-bench repo root; loads ``labs/p1-twin/twin.py``

The resolved predictor is **cached** for the process. If ``ASML_BENCH_ROOT`` /
``ASML_P1_TWIN_PATH`` change mid-process, call
``get_predict_twin(force_reload=True)`` or ``reset_loader_cache()`` so the new
path is picked up.

Product researchers should ``from asml_product_p1_twin import simulate`` and never
import the bench sandbox directly.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable

from . import reference_twin

PredictFn = Callable[[dict], dict]

_CACHED: tuple[str, PredictFn] | None = None


def _load_module_from_path(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("asml_p1_twin_sandbox", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load twin module from {path}")
    mod = importlib.util.module_from_spec(spec)
    # Avoid polluting sys.modules permanently under a conflicting name across reloads
    sys.modules["asml_p1_twin_sandbox"] = mod
    spec.loader.exec_module(mod)
    return mod


def _resolve_twin_path() -> Path | None:
    explicit = os.environ.get("ASML_P1_TWIN_PATH")
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if p.is_dir():
            p = p / "twin.py"
        return p if p.is_file() else None

    bench = os.environ.get("ASML_BENCH_ROOT")
    if bench:
        p = Path(bench).expanduser().resolve() / "labs" / "p1-twin" / "twin.py"
        return p if p.is_file() else None

    return None


def get_predict_twin(*, force_reload: bool = False) -> tuple[str, PredictFn]:
    """Return ``(source_label, predict_twin)``.

    ``source_label`` is ``"reference"`` or the resolved filesystem path string.

    Pass ``force_reload=True`` after changing ``ASML_BENCH_ROOT`` /
    ``ASML_P1_TWIN_PATH`` mid-process; otherwise the first resolution stays cached.
    """
    global _CACHED
    if _CACHED is not None and not force_reload:
        return _CACHED

    path = _resolve_twin_path()
    if path is not None:
        mod = _load_module_from_path(path)
        if not hasattr(mod, "predict_twin"):
            raise AttributeError(f"{path} has no predict_twin")
        _CACHED = (str(path), mod.predict_twin)
        return _CACHED

    _CACHED = ("reference", reference_twin.predict_twin)
    return _CACHED


def reset_loader_cache() -> None:
    """Test helper: clear cached predictor."""
    global _CACHED
    _CACHED = None
