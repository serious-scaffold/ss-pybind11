from __future__ import annotations

from importlib_metadata import version

import ss_pybind11 as m


def test_version():
    assert version("ss_pybind11") == m.__version__
