import pytest
from fastapi.testclient import TestClient
from atropos.main import app


@pytest.fixture
def client():
    return TestClient(app)
