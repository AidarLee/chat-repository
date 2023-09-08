from fastapi import FastAPI
from sqlalchemy import create_engine, and_, func, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from models import *
from schemas import *
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import aliased

engine = create_engine('postgresql://postgres:123@127.0.0.1/chat')

app = FastAPI()

Session = sessionmaker(bind=engine)
session = Session()

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user):
        try:
            self.session.add(user)
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def read(self, user_id):
        try:
            return self.session.query(User).filter_by(id=user_id).first()
        except Exception as e:
            raise e
        
    def get_all_users(self):
        try:
            return self.session.query(User).all()
        except Exception as e:
            raise e
        
    def get_user_by_id(self, user_id=None, username=None):
        try:
            if user_id:
                return self.session.query(User).filter_by(id=user_id).one()
            elif username:
                return self.session.query(User).filter_by(username=username).one()
        except NoResultFound:
            return None
        except Exception as e:
            raise e
        
    def get_chats_with_user(self, user_id, status=None):
        try:
            query = self.session.query(Chat, User.username)\
                .join(UserChat, Chat.id == UserChat.chat_id)\
                .join(User, UserChat.user_id == User.id)\
                .filter(UserChat.user_id == user_id)

            if status is not None:
                query = query.filter(Chat.status == status)

            result = query.all()

            chats_with_users = [UserChatsSchema(
                chat_id=chat.id,
                chat_name=chat.name,
                status=chat.status,
                user_id=user.id,
                username=user.username
            ) for chat, user in result]

            return ChatWithUsersResponse(chats=chats_with_users)
        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, user):
        try:
            self.session.merge(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        
    def delete(self, user):
        try:
            self.session.delete(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
            
user_repository = UserRepository(Session())

class ChatRepository:
    def __init__(self, db_session: Session):
        self.session = db_session

    def create(self, chat):
        try:
            self.session.add(chat)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        
    def read(self, chat_id):
        try:
            return self.session.query(Chat).filter_by(id=chat_id).first()
        except Exception as e:
            raise e
        
    def update(self, chat):
        try:
            self.session.merge(chat)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, chat):
        try:
            self.session.delete(chat)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        
    def get_total_chat_count_for_users(self, user_id1, user_id2, status=None):
        try:
            query = self.session.query(func.count(Chat.id)) \
                .join(UserChat, Chat.id == UserChat.chat_id) \
                .filter(UserChat.user_id == user_id1) \
                .filter(UserChat.user_id == user_id2)

            if status is not None:
                query = query.filter(Chat.status == status)

            total_count = query.scalar()
            return total_count
            
        except Exception as e:
            self.session.rollback()
            raise e


chat_repository = ChatRepository(Session())

class UserChatRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create(self, userchat):
        try:
            self.db_session.add(userchat)
            self.db_session.commit()
            return userchat
        except Exception as e:
            self.db_session.rollback()
            raise e

    def read(self, userchat_id):
        try:
            return self.db_session.query(UserChat).filter_by(id=userchat_id).first()
        except Exception as e:
            raise e

    def update(self, userchat):
        try:
            self.db_session.merge(userchat)
            self.db_session.commit()
            return userchat
        except Exception as e:
            self.db_session.rollback()
            raise e

    def delete(self, userchat):
        try:
            self.db_session.delete(userchat)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e
        
    def get_total_message_count(self, chat_id):
        try:
            total_message_count = self.db_session.query(func.sum(UserChat.message_count))\
                .filter(UserChat.chat_id == chat_id)\
                .scalar()

            return total_message_count
        except SQLAlchemyError as e:
            raise e

userchat_repository = UserChatRepository(Session())

class MessagesRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, message):
        try:
            self.db_session.add(message)
            self.db_session.commit()

            chat_id = message.chat_id
            user_chat_alias = aliased(UserChat)
            update_statement = update(UserChat).where(UserChat.chat_id == chat_id).values(
                message_count=UserChat.message_count + 1
            )

            self.db_session.execute(update_statement)
            self.db_session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, message):
        try:
            self.db_session.delete(message)
            self.db_session.commit()

            chat_id = message.chat_id
            user_chat_alias = aliased(UserChat)
            update_statement = update(UserChat).where(UserChat.chat_id == chat_id).values(
                message_count=UserChat.message_count - 1
            )

            self.db_session.execute(update_statement)
            self.db_session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def get_messages(self, sender_id=None, receiver_id=None, time_delivered=None):
        try:
            messages_query = self.db_session.query(Message)
            if sender_id:
                messages_query = messages_query.filter(Message.sender_id == sender_id)
            if receiver_id:
                messages_query = messages_query.filter(Message.receiver_id == receiver_id)
            if time_delivered:
                messages_query = messages_query.filter(Message.time_delivered >= time_delivered)
            return messages_query.all()
        except Exception as e:
            raise e
        
        


