import pytest
from fastapi.testclient import TestClient

from fastapi_z.app import app


@pytest.fixture
def client():
    return TestClient(app)
