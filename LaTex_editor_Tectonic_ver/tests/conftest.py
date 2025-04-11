import os
import sys
import pytest

sys.path.insert(0,  # noqa: E402
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from backend.server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
