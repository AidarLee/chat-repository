from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import List, Optional

class UserSchema(BaseModel):
    id: UUID4
    username: str
    photo_url: Optional[str]

class ChatSchema(BaseModel):
    id: int
    name: str
    status: int
    update_at: int
    users: Optional[List[UserSchema]] 

class UserChatsSchema(BaseModel):
    chat_id: UUID4
    chat_name: str
    status: int
    user_id: UUID4
    username: str

class ChatWithUsersResponse(BaseModel):
    chats: List[UserChatsSchema]

class MessageSchema(BaseModel):
    id: int
    sender: UUID4
    receiver: UUID4
    text: str
    time_delivered: datetime
    time_seen: datetime
    is_delivered: bool
    chat_id: int