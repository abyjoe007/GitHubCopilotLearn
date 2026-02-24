import sys
from pathlib import Path
import copy
import pytest
from fastapi.testclient import TestClient


# Ensure `src` directory is importable from the tests
ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import app as app_module


@pytest.fixture()
def client():
    """Yield a TestClient and restore `app.activities` after each test.

    Uses a deepcopy snapshot to keep tests isolated from each other.
    """
    snapshot = copy.deepcopy(app_module.activities)
    client = TestClient(app_module.app)
    try:
        yield client
    finally:
        app_module.activities.clear()
        app_module.activities.update(snapshot)
