from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import httpx
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter(prefix="/ai", tags=["ai"])

class ChatRequest(BaseModel):
    messages: list
    temperature: float = 0.96
    max_tokens: int = 256
    top_p: float = 1
    frequency_penalty: float = 0
    presence_penalty: float = 0

class ChatResponse(BaseModel):
    responses: list

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    api_key = "API Key"  # API Key는 환경 변수 등으로 관리하는 것이 보안상 안전합니다.
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4-turbo",
        "messages": request.messages,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "top_p": request.top_p,
        "frequency_penalty": request.frequency_penalty,
        "presence_penalty": request.presence_penalty
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to communicate with OpenAI API")
        results = response.json()
        return ChatResponse(responses=results['choices'])

    return ChatResponse(responses=[])  # 실패 시 빈 응답 반환
