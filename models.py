from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class PersonalityTypeEnum(enum.Enum):
    ISTJ = "ISTJ"
    ISTP = "ISTP"
    ISFJ = "ISFJ"
    ISFP = "ISFP"
    INTJ = "INTJ"
    INTP = "INTP"
    INFJ = "INFJ"
    INFP = "INFP"
    ESTJ = "ESTJ"
    ESTP = "ESTP"
    ESFJ = "ESFJ"
    ESFP = "ESFP"
    ENTJ = "ENTJ"
    ENTP = "ENTP"
    ENFJ = "ENFJ"
    ENFP = "ENFP"

class User(Base):
    __tablename__ = "user"
    userId = Column(Integer, primary_key=True, index=True)
    accountId = Column(String(50), unique=True, index=True)
    name = Column(String(50))
    password = Column(String(100))
    age = Column(Integer)
    personalityType = Column(Enum(PersonalityTypeEnum))

class AiCharacter(Base):
    __tablename__ = "aicharacter"
    characterId = Column(Integer, primary_key=True, index=True)
    aiName = Column(String(50))
    description = Column(Text)
    difficultyLevel = Column(Integer)

class Conversation(Base):
    __tablename__ = "conversation"
    conversationId = Column(Integer, primary_key=True, index=True)
    day = Column(DateTime)
    userId = Column(Integer, ForeignKey("user.userId"))
    characterId = Column(Integer, ForeignKey("aicharacter.characterId"))

    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "message"
    messageId = Column(Integer, primary_key=True, index=True)
    conversationId = Column(Integer, ForeignKey("conversation.conversationId"), nullable=False)
    sender = Column(Boolean, nullable=False)
    messageText = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
    ai_response = relationship("AIResponse", back_populates="message", foreign_keys="[AIResponse.aiMessage]")  # 외래 키 명시

class AIResponse(Base):
    __tablename__ = "AIRresponses"
    aiMessage = Column(Integer, ForeignKey("message.messageId"), primary_key=True, index=True)
    text = Column(Text, nullable=False)
    feeling = Column(Text)
    affinity_score = Column(Integer)
    achieved_quest = Column(Text)
    rejection_score = Column(Integer)
    userMessage = Column(Text)
    conversation_id = Column(Integer, ForeignKey("message.conversationId"))
    rejection_content = Column(Text)
    final_rejection_score = Column(Integer)

    message = relationship("Message", back_populates="ai_response", foreign_keys=[aiMessage])  # 외래 키 명시

class Tip(Base):
    __tablename__ = "tip"
    tipId = Column(Integer, primary_key=True, index=True)
    messageId = Column(Integer, ForeignKey("message.messageId"))
    tipText = Column(Text)

class Liking(Base):
    __tablename__ = "liking"
    likingId = Column(Integer, primary_key=True, index=True)
    messageId = Column(Integer, ForeignKey("message.messageId"))
    likingLevel = Column(Integer)
    characterId = Column(Integer, ForeignKey("aicharacter.characterId"))
    userId = Column(Integer, ForeignKey("user.userId"))

class Mindset(Base):
    __tablename__ = "mindset"
    mindsetId = Column(Integer, primary_key=True, index=True)
    mindsetText = Column(Text)

class Feedback(Base):
    __tablename__ = "feedback"
    feedbackId = Column(Integer, primary_key=True, index=True)
    conversationId = Column(Integer, ForeignKey("conversation.conversationId"))
    feedbackText = Column(Text)
    finalLikingLevel = Column(Integer)
    totalRejectionScore = Column(Integer)

class Rejection(Base):
    __tablename__ = "rejection"
    rejectionId = Column(Integer, primary_key=True, index=True)
    messageId = Column(Integer, ForeignKey("message.messageId"))
    rejectionLevel = Column(Integer)
    characterId = Column(Integer, ForeignKey("aicharacter.characterId"))
    userId = Column(Integer, ForeignKey("user.userId"))
    rejectionText = Column(Text)

class UserCollection(Base):
    __tablename__ = "usercollection"
    userId = Column(Integer, ForeignKey("user.userId"), primary_key=True)
    characterId = Column(Integer, ForeignKey("aicharacter.characterId"), primary_key=True)
    addedDate = Column(DateTime)

class Emotion(Base):
    __tablename__ = "emotion"
    emotionId = Column(Integer, primary_key=True, index=True)
    emotionType = Column(String(50))
    vibrationPattern = Column(Integer)
    backgroundColor = Column(String(20))
    messageId = Column(Integer, ForeignKey("message.messageId"))
