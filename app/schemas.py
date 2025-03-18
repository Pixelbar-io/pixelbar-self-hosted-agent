from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid


class FlashMessage(BaseModel):
    """Schema for flash message requests."""

    title: str = Field(..., description="Title of the message")
    content: str = Field(..., description="Content of the message")
    type: str = Field("info", description="Type of message (info, warning, error)")
    duration_seconds: Optional[int] = Field(
        10, description="Duration in seconds to display the message"
    )
    priority: int = Field(1, description="Priority of the message (1-5)")


class FlashMessageInDB(BaseModel):
    """Schema for flash messages in the database."""

    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    screen_id: str
    message: str
    type: str
    number_of_replays: int = 0
    created: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class FlashMessageResponse(BaseModel):
    """Schema for flash message responses."""

    uuid: str
    screen_id: str
    message: str
    type: str
    number_of_replays: int
    created: datetime

    class Config:
        from_attributes = True


class FlashMessageListResponse(BaseModel):
    """Schema for a list of flash messages."""

    messages: List[FlashMessageResponse]
    total: int

    class Config:
        from_attributes = True


class HotData(BaseModel):
    """Schema for hot data responses."""

    screen_id: str = Field(..., description="ID of the screen")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Timestamp of the data"
    )
    data: Dict[str, Any] = Field(..., description="Actual hot data content")


class HotDataInDB(BaseModel):
    """Schema for hot data in the database."""

    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sequence_id: int
    widget_id: str
    json_data: Dict[str, Any]
    created: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class StatusResponse(BaseModel):
    """Schema for status responses."""

    status: str = Field(..., description="Status of the operation")
    message: str = Field(..., description="Status message")
    screen_id: Optional[str] = Field(
        None, description="ID of the affected screen if applicable"
    )
