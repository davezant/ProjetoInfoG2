import re
from fastapi import APIRouter, Request

router = APIRouter()

def init_plugin(app):
    """
    Plugin for input data sanitization.
    """
    app.include_router(router, prefix="/sanitization", tags=["sanitization"])

def sanitize_text(text: str) -> str:
    """
    Remove potentially dangerous characters and HTML tags.
    """
    # Remove HTML tags
    sanitized = re.sub(r'<[^>]*?>', '', text)
    # Remove script-like patterns
    sanitized = re.sub(r'(javascript:|on\w+=)', '', sanitized, flags=re.IGNORECASE)
    # Remove special SQL characters
    sanitized = re.sub(r"(['\";--])", '', sanitized)
    return sanitized

@router.post("/text")
async def sanitize_endpoint(request: Request):
    """
    Sanitizes a text input in JSON: { "text": "..." }
    """
    data = await request.json()
    text = data.get("text", "")
    sanitized = sanitize_text(text)
    return {"sanitized": sanitized}
