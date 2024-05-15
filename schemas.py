from typing import Optional
from pydantic import BaseModel

class ConversationCreateResponse(BaseModel):
    conversation_id: int
