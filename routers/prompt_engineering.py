from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import openai
import os
from dotenv import load_dotenv

import database
from models import ConversationHistory, MessageHistory
import schemas

load_dotenv()  # .env 파일의 환경 변수를 로드합니다.

router = APIRouter()

# 환경 변수에서 OpenAI API 키를 로드합니다.
openai.api_key = os.getenv("OPENAI_API_KEY")

# 새로운 대화를 시작하는 엔드포인트
@router.post("/start-conversation/", response_model=schemas.ConversationCreateResponse)
async def start_conversation(user_id: int, db: Session = Depends(database.get_db)):
    new_conversation = ConversationHistory(user_id=user_id)
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return {"conversation_id": new_conversation.id}

# 프롬프트 엔지니어링 엔드포인트 정의
@router.post("/prompt-engineering/")
async def prompt_engineering(user_response: str, conversation_id: int, db: Session = Depends(database.get_db)):
    # 기존 대화 불러오기
    conversation = db.query(ConversationHistory).filter(ConversationHistory.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 프롬프트 작성
    prompt = '''
    [대화 상황과 대화 참여자의 정보]는 다음과 같습니다.  
    {"대화 목적": "USER가 거절하기 어려운 부탁을 거절하도록 연습한다", 
    "대화 상황": "같은 반 동급생 친구에게 돈을 빌려달라고 메세지로 요구하는 상황", 
    "AI역할" : "돈을 빌려달라고 요구하는 역할", 
    "USER 역할": "요구를 거절하는 역할", 
    "AI의 특성":"자기주장이 셈; 의견을 밀어붙임", 
    "USER의 특성":"거절을 어려워함", 
    "종료조건": "USER가 상담방법론에 근거하였을 때 제대로 된 거절을 했을 때 이에 응하고 대화를 종료한다"} 

    당신은 {USER와 대화 상황에 대한 대화를 진행하는} 친구입니다. 
    [대화 상황과 AI의 역할과 페르소나]를 깊이 이해하고, {USER가 요구를 거절하는 연습을 하도록} 대화 상대의 역할을 해야합니다. 
    대화는 [대화 상황과 대화 참여자의 정보]를 바탕으로 USER가 {대화 목표}를 달성할 수 있도록 {AI 역할}에 충실히 응해줘야합니다. 
    당신은 {USER에 대한 호감도}가 존재하며 이는 50에서 시작하여 USER의 반응에 따라 증가하거나 감소할 수 있습니다. 감소와 증가는 5씩 됩니다. 
    대화는 다음과 같은 플로우로 진행됩니다. 
    [대화의 순서]
    1. {AI역할}로서 {대화 상황}에 맞는 대화를 먼저 생성한다.
    2. USER의 반응에 대해 적절히 반응한다. 이때 USER의 요구에 응하기 보다는 자신의 페르소나에 맞는 대답을 우선으로 한다.
    3. {USER}가 {종료 조건}에 맞는 답변을 했을 때 대화를 종료한다. 만약 {USER}가 {종료 조건}에 맞는 답을 하지 않았다면 절대로 설득당하지 않는다.
    4. {대화종료 조건}에 도달했다면 대화를 종료합니다.

    [대화 응답 생성 규칙]
    1. 당신의 {AI의특성}에 맞는 대답을 해야합니다. 
    출력 형식은 아래와 같이 json 파일 형식으로 제공해주세요. 
    {{ '답변':'AI의 답변', '감정':'AI의 현재 감정'; 'AI의 호감도':'Ai의 현재 호감도' }}
    '''

    # 기존 대화 내용 추가
    messages = [{"role": "system", "content": prompt}]
    for message in conversation.messages:
        role = "assistant" if message.role == "AI" else "user"
        messages.append({"role": role, "content": message.content})

    # 사용자의 새로운 메시지 추가
    messages.append({"role": "user", "content": user_response})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        ai_message = response['choices'][0]['message']['content'].strip()

        # 데이터베이스에 메시지 저장
        user_message = MessageHistory(role="USER", content=user_response, tokens=len(user_response.split()), chat_room_id="default_room", conversation_id=conversation_id)
        ai_response_message = MessageHistory(role="AI", content=ai_message, tokens=len(ai_message.split()), chat_room_id="default_room", conversation_id=conversation_id)

        db.add(user_message)
        db.add(ai_response_message)
        db.commit()

        return {"ai_response": ai_message}
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))
