from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.schemas import FlashMessage, HotData, StatusResponse
from app.utils import validate_screen_id, log_api_request, logger

router = APIRouter()


@router.post("/{screen_id}/flash-message/", response_model=StatusResponse)
async def flash_message(screen_id: str, message: FlashMessage) -> Dict[str, Any]:
    """
    Endpoint to handle flash messages for a specific screen.

    Args:
        screen_id: The ID of the target screen
        message: The message data to be processed

    Returns:
        StatusResponse with success status
    """
    # Log the request
    log_api_request("flash-message", screen_id, message.model_dump())

    # Validate screen_id
    if not validate_screen_id(screen_id):
        raise HTTPException(status_code=400, detail="Invalid or missing screen ID")

    # Process message (placeholder for actual implementation)
    # This would typically include validation, storing, and forwarding logic
    logger.info(f"Processing flash message for screen {screen_id}: {message.title}")

    return StatusResponse(
        status="success", message="Flash message received", screen_id=screen_id
    )


@router.get("/{screen_id}/hotdata/", response_model=HotData)
async def get_hotdata(screen_id: str) -> Dict[str, Any]:
    """
    Endpoint to retrieve hot data for a specific screen.

    Args:
        screen_id: The ID of the target screen

    Returns:
        HotData containing the hot data for the specified screen
    """
    # Log the request
    log_api_request("hotdata", screen_id)

    # Validate screen_id
    if not validate_screen_id(screen_id):
        raise HTTPException(status_code=400, detail="Invalid or missing screen ID")

    # Fetch hot data (placeholder for actual implementation)
    # This would typically include database queries or other data sources
    logger.info(f"Fetching hot data for screen {screen_id}")

    # Sample response data
    hot_data = HotData(
        screen_id=screen_id,
        data={"temperature": 23.5, "humidity": 45, "notifications": 3},
    )

    return hot_data
