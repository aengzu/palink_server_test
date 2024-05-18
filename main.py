from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import (
    Base, User, CharacterData, Conversation, Message, Tip, Feedback, Collection, Emotion, Mindset, Liking, Rejection
)
from schemas import (
    UserCreate, UserResponse, LoginRequest, LoginResponse, ConversationCreate, ConversationResponse, MessageCreate,
    MessageResponse, TipCreate, TipResponse, CharacterResponse, FeedbackCreate, FeedbackResponse, CollectionCreate,
    CollectionResponse, EmotionResponse, EmotionCreate, MindsetResponse, MindsetCreate, LikingCreate, LikingResponse,
    RejectionCreate, RejectionResponse
)
from database import engine, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Routes for User
@app.post("/api/user/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/user/login", response_model=LoginResponse)
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == login.user_id, User.password == login.password).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return db_user

@app.get("/api/user/get", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Routes for Conversation
@app.post("/api/conversation/create", response_model=ConversationResponse)
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    db_conversation = Conversation(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@app.get("/api/conversation/get_by_user_id", response_model=List[ConversationResponse])
def get_conversations_by_user_id(user_id: str, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()
    return conversations

@app.get("/api/conversation/get_by_conversation_id", response_model=ConversationResponse)
def get_conversation_by_conversation_id(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

# Routes for Message
@app.post("/api/message/create", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/api/message/get_by_message_id", response_model=MessageResponse)
def get_message_by_message_id(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.message_id == message_id).first()
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@app.get("/api/message/get_by_conversation_id", response_model=List[MessageResponse])
def get_messages_by_conversation_id(conversation_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return messages

# Routes for Tip
@app.post("/api/tip/create", response_model=TipResponse)
def create_tip(tip: TipCreate, db: Session = Depends(get_db)):
    db_tip = Tip(**tip.dict())
    db.add(db_tip)
    db.commit()
    db.refresh(db_tip)
    return db_tip

@app.get("/api/tip/get", response_model=TipResponse)
def get_tip(tip_id: int, db: Session = Depends(get_db)):
    tip = db.query(Tip).filter(Tip.tip_id == tip_id).first()
    if tip is None:
        raise HTTPException(status_code=404, detail="Tip not found")
    return tip

# Routes for Character
@app.get("/api/character/get", response_model=CharacterResponse)
def get_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(CharacterData).filter(CharacterData.character_id == character_id).first()
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

# Routes for Feedback
@app.post("/api/feedback/create", response_model=FeedbackResponse)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/api/feedback/get_by_conversation_id", response_model=FeedbackResponse)
def get_feedback_by_conversation_id(conversation_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.conversation_id == conversation_id).first()
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

# Routes for Collection
@app.post("/api/collection/character/create", response_model=CollectionResponse)
def create_collection(collection: CollectionCreate, db: Session = Depends(get_db)):
    db_collection = Collection(**collection.dict())
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection

@app.get("/api/collection/character/get", response_model=List[CollectionResponse])
def get_collection_by_user_id(user_id: str, db: Session = Depends(get_db)):
    collections = db.query(Collection).filter(Collection.user_id == user_id).all()
    return collections

# Routes for Emotion
@app.get("/api/emotion/get", response_model=EmotionResponse)
def get_emotion(emotion_id: int, db: Session = Depends(get_db)):
    emotion = db.query(Emotion).filter(Emotion.emotion_id == emotion_id).first()
    if emotion is None:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return emotion

@app.post("/api/emotion/create", response_model=EmotionResponse)
def create_emotion(emotion: EmotionCreate, db: Session = Depends(get_db)):
    db_emotion = Emotion(**emotion.dict())
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)
    return db_emotion

# Routes for Mindset
@app.get("/api/mindset/get", response_model=MindsetResponse)
def get_mindset(mindset_id: int, db: Session = Depends(get_db)):
    mindset = db.query(Mindset).filter(Mindset.mindset_id == mindset_id).first()
    if mindset is None:
        raise HTTPException(status_code=404, detail="Mindset not found")
    return mindset

@app.post("/api/mindset/create", response_model=MindsetResponse)
def create_mindset(mindset: MindsetCreate, db: Session = Depends(get_db)):
    db_mindset = Mindset(**mindset.dict())
    db.add(db_mindset)
    db.commit()
    db.refresh(db_mindset)
    return db_mindset

# Routes for Liking
@app.post("/api/liking/create", response_model=LikingResponse)
def create_liking(liking: LikingCreate, db: Session = Depends(get_db)):
    db_liking = Liking(**liking.dict())
    db.add(db_liking)
    db.commit()
    db.refresh(db_liking)
    return db_liking

@app.get("/api/liking/get_by_user_and_character", response_model=LikingResponse)
def get_liking_by_user_and_character(user_id: str, character_id: int, db: Session = Depends(get_db)):
    liking = db.query(Liking).filter(Liking.user_id == user_id, Liking.character_id == character_id).first()
    if liking is None:
        raise HTTPException(status_code=404, detail="Liking not found")
    return liking

# Routes for Rejection
@app.post("/api/rejection/create", response_model=RejectionResponse)
def create_rejection(rejection: RejectionCreate, db: Session = Depends(get_db)):
    db_rejection = Rejection(**rejection.dict())
    db.add(db_rejection)
    db.commit()
    db.refresh(db_rejection)
    return db_rejection

@app.get("/api/rejection/get_by_user_and_character", response_model=RejectionResponse)
def get_rejection_by_user_and_character(user_id: str, character_id: int, db: Session = Depends(get_db)):
    rejection = db.query(Rejection).filter(Rejection.user_id == user_id, Rejection.character_id == character_id).first()
    if rejection is None:
        raise HTTPException(status_code=404, detail="Rejection not found")
    return rejection

@app.get("/api/rejection/get_by_message_id", response_model=RejectionResponse)
def get_rejection_by_message_id(message_id: int, db: Session = Depends(get_db)):
    rejection = db.query(Rejection).filter(Rejection.message_id == message_id).first()
    if rejection is None:
        raise HTTPException(status_code=404, detail="Rejection not found")
    return rejection
