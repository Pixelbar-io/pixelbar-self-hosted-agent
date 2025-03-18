import pytest
from app.schemas import FlashMessage

def test_root_endpoint(test_client):
    """Test the root endpoint returns the correct structure."""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert data["name"] == "pixelbar-agent"
    assert "version" in data

def test_flash_message_endpoint(test_client, sample_screen_id, sample_flash_message):
    """Test the flash message endpoint with valid data."""
    response = test_client.post(
        f"/api/{sample_screen_id}/flash-message/", 
        json=sample_flash_message
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["screen_id"] == sample_screen_id

def test_flash_message_validation(test_client, sample_screen_id):
    """Test the flash message endpoint with invalid data."""
    # Missing required fields
    invalid_message = {
        "type": "info",
        "duration_seconds": 15,
    }
    
    response = test_client.post(
        f"/api/{sample_screen_id}/flash-message/", 
        json=invalid_message
    )
    assert response.status_code == 422  # Validation error

def test_hotdata_endpoint(test_client, sample_screen_id):
    """Test the hotdata endpoint."""
    response = test_client.get(f"/api/{sample_screen_id}/hotdata/")
    assert response.status_code == 200
    data = response.json()
    assert data["screen_id"] == sample_screen_id
    assert "data" in data
    assert "timestamp" in data 