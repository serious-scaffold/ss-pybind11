from __future__ import annotations

from ss_pybind11 import _core


def test_core_version():
    assert _core.version() != ""
