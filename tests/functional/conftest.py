import uuid
import pytest
from fastapi.testclient import TestClient
from src.controllers.api import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"
