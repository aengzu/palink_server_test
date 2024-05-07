from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import SessionLocal
from models import Chatroom, ChatMessage, Users

router = APIRouter(prefix="/chat", tags=["chat"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatroomBase(BaseModel):
    chatroom_name: str
    status: str

class ChatroomCreate(ChatroomBase):
    user_id: int  # Chatroom 생성자의 사용자 ID

class ChatroomRead(ChatroomBase):
    chatroom_id: int
    user_id: int

    class Config:
        orm_mode = True

class ChatMessageCreate(BaseModel):
    message_content: str
    user_id: int  # 메시지를 보내는 사용자 ID

class ChatMessageRead(ChatMessageCreate):
    message_id: int
    creation_date: str

    class Config:
        orm_mode = True

# 채팅방 생성
@router.post("/rooms", response_model=ChatroomRead, status_code=201)
async def create_chatroom(room_data: ChatroomCreate, db: Session = Depends(get_db)):
    new_room = Chatroom(**room_data.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

# 모든 채팅방 조회
@router.get("/rooms", response_model=List[ChatroomRead])
async def read_chatrooms(db: Session = Depends(get_db)):
    rooms = db.query(Chatroom).all()
    return rooms

# 채팅방 내 메시지 조회
@router.get("/rooms/{chatroom_id}/messages", response_model=List[ChatMessageRead])
async def read_messages(chatroom_id: int, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(ChatMessage.chatroom_id == chatroom_id).all()
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found in the chatroom")
    return messages

# 채팅방에 메시지 보내기
@router.post("/rooms/{chatroom_id}/messages", response_model=ChatMessageRead, status_code=201)
async def send_message(chatroom_id: int, message_data: ChatMessageCreate, db: Session = Depends(get_db)):
    message = ChatMessage(**message_data.dict(), chatroom_id=chatroom_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

# 채팅방 삭제
@router.delete("/rooms/{chatroom_id}", status_code=204)
async def delete_chatroom(chatroom_id: int, db: Session = Depends(get_db)):
    room = db.query(Chatroom).filter(Chatroom.chatroom_id == chatroom_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    db.delete(room)
    db.commit()
    return {"detail": "Chatroom deleted successfully"}
