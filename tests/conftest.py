import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def test_client():
    """Fixture that provides a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def sample_screen_id():
    """Fixture that provides a sample screen ID for testing."""
    return "screen123"

@pytest.fixture
def sample_flash_message():
    """Fixture that provides a sample flash message for testing."""
    return {
        "title": "Test Message",
        "content": "This is a test message",
        "type": "info",
        "duration_seconds": 15,
        "priority": 2
    } 