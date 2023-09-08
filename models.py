from sqlalchemy import Column, Integer, SmallInteger, DateTime, VARCHAR, ForeignKey, Boolean, create_engine, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import text, func
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

engine = create_engine('postgresql://postgres:123@127.0.0.1/chat')

class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(VARCHAR, nullable=False)
    status = Column(SmallInteger, nullable=False)
    update_at = Column(DateTime, nullable=False)
    
    userchats = relationship("UserChat", back_populates="chat")
    messages = relationship("Message", back_populates="chat")

class UserChat(Base):
    __tablename__ = 'userchats'

    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    message_count = Column(Integer, default=0)  

    chat = relationship("Chat", back_populates="userchats")
    user = relationship("User", back_populates="userchats")

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    text = Column(VARCHAR, nullable=False)
    time_delivered = Column(DateTime, nullable=False)
    time_seen = Column(DateTime, nullable=False)
    is_delivered = Column(Boolean, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="messages_received")
    chat = relationship("Chat", back_populates="messages")

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, unique=True, server_default=text("gen_random_uuid()"))
    username = Column(VARCHAR, nullable=False, unique=True)
    photo_url = Column(VARCHAR)

    messages_sent = relationship("Message", foreign_keys=[Message.sender_id], back_populates="sender")
    messages_received = relationship("Message", foreign_keys=[Message.receiver_id], back_populates="receiver")
    userchats = relationship("UserChat", back_populates="user")

Base.metadata.create_all(engine)