import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("pixelbar-agent")


def validate_screen_id(screen_id: str) -> bool:
    """
    Validate a screen ID.

    Args:
        screen_id: The ID to validate

    Returns:
        bool: True if valid, False otherwise
    """
    # Placeholder for actual validation logic
    # This could check against a database of registered screens
    return bool(screen_id and screen_id.strip())


def log_api_request(
    endpoint: str, screen_id: str, data: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log an API request.

    Args:
        endpoint: The endpoint being called
        screen_id: The screen ID in the request
        data: Optional request data
    """
    logger.info(f"API Request: {endpoint} - Screen ID: {screen_id}")
    if data:
        logger.debug(f"Request Data: {data}")


def handle_error(error_msg: str, status_code: int = 500) -> Dict[str, Any]:
    """
    Handle an error and return a standardized error response.

    Args:
        error_msg: The error message
        status_code: HTTP status code

    Returns:
        Dict with error information
    """
    logger.error(f"Error: {error_msg} (Status Code: {status_code})")
    return {"status": "error", "message": error_msg, "code": status_code}
