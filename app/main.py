import os
import subprocess
import uuid
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Query
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.api.endpoints import router as api_router
from app.database import (
    get_db,
    create_tables,
    FlashMessage as DBFlashMessage,
    HotData as DBHotData,
)
from app.schemas import (
    FlashMessageInDB,
    FlashMessageResponse,
    FlashMessageListResponse,
    HotDataInDB,
)

# Initialize FastAPI app
app = FastAPI(
    title="Pixelbar Self HostedAgent",
    description="On-premises agent for Pixelbar",
    version="0.1.0",
)

# Create database tables
create_tables()


def get_git_hash() -> str:
    """Get the current git commit hash from environment variable."""
    return os.getenv("GIT_HASH", "unknown")


async def verify_api_key(api_key: str = Query(None, alias="api-key")):
    """Verify that the API key is valid."""
    # Get the valid API key from environment variable - this is more secure than hardcoding
    valid_api_key = os.getenv("PIXELBAR_API_KEY")

    if valid_api_key and not api_key:
        raise HTTPException(status_code=401, detail="API key is required")

    if api_key != valid_api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return api_key


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint returning version information."""
    return {
        "name": "pixelbar-agent",
        "description": "On-premises agent for Pixelbar",
        "url": "https://app.pixelbar.io/api-docs/agent-intro/",
        "version": get_git_hash(),
    }


# Include API routes with API key protection
app.include_router(api_router, prefix="/api", dependencies=[Depends(verify_api_key)])


@app.post("/api/{screen_id}/flash-messages/")
async def flash_message(
    screen_id: str,
    message: Dict[str, Any],
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Endpoint to handle flash messages for a specific screen.

    Args:
        screen_id: The ID of the target screen
        message: The message data to be processed
        api_key: API key for authentication
        db: Database session

    Returns:
        Dict containing operation status
    """
    # Validate screen_id
    if not screen_id:
        raise HTTPException(status_code=400, detail="Screen ID is required")

    # Extract message text from the payload
    message_text = message.get("message", "")
    if not message_text:
        raise HTTPException(status_code=400, detail="Message text is required")

    # Create a new flash message
    db_message = DBFlashMessage(
        uuid=str(uuid.uuid4()),
        screen_id=screen_id,
        message=message_text,  # Store only the message text
        type=message.get("message_type", "info"),
        number_of_replays=message.get("number_of_replays", 0),
    )

    # Add to database
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return {
        "status": "success",
        "screen_id": screen_id,
        "message": "Flash message stored successfully",
        "uuid": db_message.uuid,
    }


@app.get("/api/{screen_id}/flash-messages/", response_model=FlashMessageListResponse)
async def get_flash_messages(
    screen_id: str,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db),
) -> FlashMessageListResponse:
    """
    Endpoint to retrieve flash messages for a specific screen.

    Args:
        screen_id: The ID of the target screen
        api_key: API key for authentication
        db: Database session

    Returns:
        List of flash messages for the specified screen
    """
    # Validate screen_id
    if not screen_id:
        raise HTTPException(status_code=400, detail="Screen ID is required")

    # Get messages from database (max 50, ordered by created desc)
    messages = (
        db.query(DBFlashMessage)
        .filter(DBFlashMessage.screen_id == screen_id)
        .order_by(DBFlashMessage.created.desc())
        .limit(50)
        .all()
    )

    # Convert messages to response format
    response_messages = []
    for msg in messages:
        msg_dict = {
            "uuid": msg.uuid,
            "screen_id": msg.screen_id,
            "message": msg.message,  # Now this is just the message text
            "type": msg.type,
            "number_of_replays": msg.number_of_replays,
            "created": msg.created,
        }
        response_messages.append(msg_dict)

    return {"messages": response_messages, "total": len(response_messages)}


@app.post("/api/{screen_id}/hotdata/")
async def create_hotdata(
    screen_id: str,
    widget_id: str,
    data: Dict[str, Any],
    sequence_id: int = 0,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Endpoint to store hot data for a specific screen and widget.

    Args:
        screen_id: The ID of the target screen
        widget_id: The ID of the widget
        data: The hot data to be stored
        sequence_id: Sequence ID for ordering
        api_key: API key for authentication
        db: Database session

    Returns:
        Dict containing operation status
    """
    # Validate screen_id and widget_id
    if not screen_id:
        raise HTTPException(status_code=400, detail="Screen ID is required")
    if not widget_id:
        raise HTTPException(status_code=400, detail="Widget ID is required")

    # Create a new hot data entry
    db_hotdata = DBHotData(
        uuid=str(uuid.uuid4()),
        sequence_id=sequence_id,
        widget_id=widget_id,
        json_data=json.dumps(data),
    )

    # Add to database
    db.add(db_hotdata)
    db.commit()
    db.refresh(db_hotdata)

    return {
        "status": "success",
        "screen_id": screen_id,
        "widget_id": widget_id,
        "message": "Hot data stored successfully",
        "uuid": db_hotdata.uuid,
    }


@app.get("/api/{screen_id}/hotdata/")
async def get_hotdata(
    screen_id: str,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Endpoint to retrieve hot data for a specific screen.

    Args:
        screen_id: The ID of the target screen
        api_key: API key for authentication
        db: Database session

    Returns:
        Dict containing the hot data for the specified screen
    """
    # Validate screen_id
    if not screen_id:
        raise HTTPException(status_code=400, detail="Screen ID is required")

    # Get latest hot data for all widgets associated with this screen
    widget_data = {}

    # Get all unique widget IDs for this screen
    widgets = db.query(DBHotData.widget_id).distinct().all()

    # For each widget, get the latest data
    for widget in widgets:
        widget_id = widget[0]
        latest_data = (
            db.query(DBHotData)
            .filter(DBHotData.widget_id == widget_id)
            .order_by(DBHotData.sequence_id.desc())
            .first()
        )

        if latest_data:
            widget_data[widget_id] = json.loads(latest_data.json_data)

    return {
        "screen_id": screen_id,
        "timestamp": datetime.utcnow().isoformat(),
        "data": widget_data,
    }
