from pydantic import BaseModel
from datetime import datetime

# Pydantic models
class UserCreate(BaseModel):
    user_id: str
    name: str
    password: str
    age: int
    personality_type: str

class UserResponse(BaseModel):
    user_id: str
    name: str
    age: int
    personality_type: str

class LoginRequest(BaseModel):
    user_id: str
    password: str

class LoginResponse(BaseModel):
    user_id: str
    name: str
    age: int
    personality_type: str

class ConversationCreate(BaseModel):
    day: datetime
    user_id: str
    character_id: int

class ConversationResponse(BaseModel):
    conversation_id: int
    day: datetime
    user_id: str
    character_id: int

class MessageCreate(BaseModel):
    sender: bool
    message_text: str
    timestamp: datetime
    conversation_id: int

class MessageResponse(BaseModel):
    message_id: int
    sender: bool
    message_text: str
    timestamp: datetime
    conversation_id: int

class TipCreate(BaseModel):
    tip_text: str
    message_id: int

class TipResponse(BaseModel):
    tip_id: int
    tip_text: str
    message_id: int

class CharacterResponse(BaseModel):
    character_id: int
    difficulty_level: int
    ai_name: str
    description: str

class FeedbackCreate(BaseModel):
    feedback_text: str
    liking_level: int
    day: datetime
    conversation_id: int

class FeedbackResponse(BaseModel):
    feedback_id: int
    feedback_text: str
    liking_level: int
    day: datetime
    conversation_id: int

class CollectionCreate(BaseModel):
    user_id: str
    character_id: int
    added_date: datetime

class CollectionResponse(BaseModel):
    collection_id: int
    user_id: str
    character_id: int
    added_date: datetime

class EmotionResponse(BaseModel):
    emotion_id: int
    emotion_type: str
    vibration_pattern: str
    background_color: str

class EmotionCreate(BaseModel):
    emotion_id: int
    emotion_type: str
    vibration_pattern: str
    background_color: str

class MindsetResponse(BaseModel):
    mindset_id: int
    mindset_text: str

class MindsetCreate(BaseModel):
    mindset_id: int
    mindset_text: str

class LikingCreate(BaseModel):
    user_id: str
    character_id: int
    liking_level: int
    message_id: int

class LikingResponse(BaseModel):
    liking_id: int
    user_id: str
    character_id: int
    liking_level: int
    message_id: int

class RejectionCreate(BaseModel):
    user_id: str
    character_id: int
    rejection_level: int
    message_id: int

class RejectionResponse(BaseModel):
    rejection_id: int
    user_id: str
    character_id: int
    rejection_level: int
    message_id: int
