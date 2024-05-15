from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Text, Date, DateTime
from datetime import datetime

class MessageHistory(Base):
    __tablename__ = "message_history"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    content = Column(Text)
    tokens = Column(Integer)
    chat_room_id = Column(String, nullable=False, default="default_room")
    conversation_id = Column(Integer, ForeignKey("conversation_history.id"))

class ConversationHistory(Base):
    __tablename__ = "conversation_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    messages = relationship("MessageHistory", backref="conversation")

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    gender = Column(Enum('남성', '여성'))
    school = Column(Enum('중학교', '고등학교'))
    hashed_password = Column(String(255))
    # 다른 클래스와의 관계 설정
    mbti = relationship("Mbti", back_populates="user")
    memberServiceLogs = relationship("MemberServiceLogs", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    today_conversations = relationship("TodayConversation", back_populates="user")

class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(255))
    # Category와 Scenario는 1:N 관계
    scenarios = relationship("Scenario", back_populates="category")  # 수정

class Scenario(Base):
    __tablename__ = 'scenarios'
    scenario_id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    scenario_name = Column(String(255))
    scenario_description = Column(Text)
    creation_date = Column(Date)

    # Scenario와 Category는 N:1 관계
    category = relationship("Category", back_populates="scenarios")  # 수정
    chatrooms = relationship("Chatroom", back_populates="scenario")
    quests = relationship("Quest", back_populates="scenario")
    roles = relationship("Role", back_populates="scenario")
    tips = relationship("Tip", back_populates="scenario")
    today_conversations = relationship("TodayConversation", back_populates="scenario")

# 나머지 클래스는 그대로 유지
#
# class Scenario(Base):
#     __tablename__ = 'scenarios'
#
#     scenario_id = Column(Integer, primary_key=True, index=True)
#     category_id = Column(Integer, ForeignKey('categories.category_id'))
#     scenario_name = Column(String(255))
#     scenario_description = Column(Text)
#     creation_date = Column(Date)
#
#     # 다른 클래스와의 관계 설정
#     category = relationship("Category")
#     chatrooms = relationship("Chatroom", back_populates="scenario")
#     quests = relationship("Quest", back_populates="scenario")
#     roles = relationship("Role", back_populates="scenario")
#     tips = relationship("Tip", back_populates="scenario")
#     today_conversations = relationship("TodayConversation", back_populates="scenario")
#
# class Category(Base):
#     __tablename__ = 'categories'
#     category_id = Column(Integer, primary_key=True, index=True)
#     category_name = Column(String(255))
#     # 다른 클래스와의 관계 설정
#     scenario = relationship("Scenario", back_populates="chatrooms")
#     user = relationship("User", back_populates="chatrooms")

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    message_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # 'users'로 수정
    chatroom_id = Column(Integer, ForeignKey('chatrooms.chatroom_id'))
    message_content = Column(Text)
    creation_date = Column(DateTime, default=datetime.now)

    # User와의 관계 설정
    user = relationship("Users")

    # Chatroom과의 관계 설정
    chatroom = relationship("Chatroom")

class Chatroom(Base):
    __tablename__ = 'chatrooms'
    chatroom_id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey('scenarios.scenario_id'))  # 'scenarios'로 수정
    user_id = Column(Integer, ForeignKey('users.id'))
    chatroom_name = Column(String(255))
    status = Column(String(50))
    creation_date = Column(DateTime, default=datetime.now)

    # Scenario와의 관계 설정
    scenario = relationship("Scenario")

    # User와의 관계 설정
    user = relationship("Users")

class Mbti(Base):
    __tablename__ = 'mbti'

    person_id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)  # 'users'로 수정
    personality_name = Column(String(255))
    personality_description = Column(Text)

    # User와의 관계 설정
    user = relationship("Users", back_populates="mbti")


class MemberServiceLogs(Base):
    __tablename__ = 'member_service_logs'

    service_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)  # 'users'로 수정
    signup_date = Column(Date)
    password_change_date = Column(Date)
    last_login_date = Column(DateTime)
    login_count = Column(Integer)

    user = relationship("Users", back_populates="memberServiceLogs")

class Notification(Base):
    __tablename__ = 'notifications'

    notification_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)  # 'users'로 수정
    notification_content = Column(Text)
    created_at = Column(DateTime)

    user = relationship("Users", back_populates="notifications")

class Quest(Base):
    __tablename__ = 'quests'

    quest_id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey('scenarios.scenario_id'), primary_key=True)  # 'scenarios'로 수정
    quest_name = Column(String(255))
    quest_content = Column(Text)

    scenario = relationship("Scenario", back_populates="quests")

class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey('scenarios.scenario_id'), primary_key=True)  # 'scenarios'로 수정
    role_name = Column(String(255))
    role_description = Column(Text)

    scenario = relationship("Scenario", back_populates="roles")


class TermsAndCondition(Base):
    __tablename__ = 'terms_and_conditions'

    terms_id = Column(Integer, primary_key=True)
    agreement_status = Column(Integer)
    order_number = Column(Integer)
    content = Column(Text)
    title = Column(String(255))
    registration_datetime = Column(DateTime)
    registrant = Column(String(255))

class Tip(Base):
    __tablename__ = 'tips'

    tip_id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer,  ForeignKey('scenarios.scenario_id'), primary_key=True)  # 'scenarios'로 수정
    message_id = Column(Integer, ForeignKey('chat_messages.message_id'))
    tip_content = Column(Text)

    scenario = relationship("Scenario", back_populates="tips")

class TodayConversation(Base):
    __tablename__ = 'today_conversations'
    conversation_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)  # 'users'로 수정
    scenario_id = Column(Integer, ForeignKey('scenarios.scenario_id'))
    # 'users' 테이블과의 관계 설정
    user = relationship("Users", back_populates="today_conversations")
    # 'scenarios' 테이블과의 관계 설정
    scenario = relationship("Scenario")

