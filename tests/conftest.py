"""Pytest configuration for test import paths."""

from pathlib import Path
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers for Dual-Track TDD."""
    config.addinivalue_line("markers", "boundary: Boundary layer contract tests")
    config.addinivalue_line("markers", "domain: Domain layer invariant tests")
    config.addinivalue_line("markers", "p0: Priority 0 ??must pass before merge")
    config.addinivalue_line("markers", "p1: Priority 1 tests")
    config.addinivalue_line("markers", "p2: Priority 2 tests")
    config.addinivalue_line("markers", "integration: Boundary + Domain integration tests")
    config.addinivalue_line("markers", "regression: Regression protection suite")
