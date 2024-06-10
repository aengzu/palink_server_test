from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# SQLAlchemy models
class User(Base):
    __tablename__ = "user"
    user_id = Column(String(255), primary_key=True, index=True)  # 길이 추가
    name = Column(String(255))  # 길이 추가
    password = Column(String(255))  # 길이 추가
    age = Column(Integer)
    personality_type = Column(String(255))  # 길이 추가

class CharacterData(Base):
    __tablename__ = "character_data"
    character_id = Column(Integer, primary_key=True, index=True)
    difficulty_level = Column(Integer)
    ai_name = Column(String(255))  # 길이 추가
    description = Column(Text)

class Conversation(Base):
    __tablename__ = "conversation"
    conversation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    day = Column(DateTime)
    user_id = Column(String(255), ForeignKey("user.user_id"))  # 길이 추가
    character_id = Column(Integer, ForeignKey("character_data.character_id"))

class Message(Base):
    __tablename__ = "message"
    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sender = Column(Boolean)
    message_text = Column(Text)
    timestamp = Column(DateTime)
    conversation_id = Column(Integer, ForeignKey("conversation.conversation_id"))

class Tip(Base):
    __tablename__ = "tip"
    tip_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tip_text = Column(Text)
    message_id = Column(Integer, ForeignKey("message.message_id"))

class Feedback(Base):
    __tablename__ = "feedback"
    feedback_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    feedback_text = Column(Text)
    liking_level = Column(Integer)
    day = Column(DateTime)
    conversation_id = Column(Integer, ForeignKey("conversation.conversation_id"))

class Collection(Base):
    __tablename__ = "collection"
    collection_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("user.user_id"))  # 길이 추가
    character_id = Column(Integer, ForeignKey("character_data.character_id"))
    added_date = Column(DateTime)

class Emotion(Base):
    __tablename__ = "emotion"
    emotion_id = Column(Integer, primary_key=True, index=True)
    emotion_type = Column(String(255))  # 길이 추가
    vibration_pattern = Column(String(255))  # 길이 추가
    background_color = Column(String(255))  # 길이 추가

class Mindset(Base):
    __tablename__ = "mindset"
    mindset_id = Column(Integer, primary_key=True, index=True)
    mindset_text = Column(Text)

class Liking(Base):
    __tablename__ = "liking"
    liking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("user.user_id"))  # 길이 추가
    character_id = Column(Integer, ForeignKey("character_data.character_id"))
    liking_level = Column(Integer)
    message_id = Column(Integer, ForeignKey("message.message_id"))

class Rejection(Base):
    __tablename__ = "rejection"
    rejection_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(255), ForeignKey("user.user_id"))  # 길이 추가
    character_id = Column(Integer, ForeignKey("character_data.character_id"))
    rejection_level = Column(Integer)
    message_id = Column(Integer, ForeignKey("message.message_id"))
