from faker import Faker
from models import User, Chat, Message, UserChat

class FakeDataGenerator:
    def __init__(self):
        self.fake = Faker()

    def create_fake_user(self):
        username = self.fake.user_name()
        photo_url = self.fake.url()
        return User(username=username, photo_url=photo_url)
    
    def update_user(self, user, new_username=None, new_photo_url=None):
        if new_username:
            user.username = new_username
        if new_photo_url:
            user.photo_url = new_photo_url
        return user

    def create_fake_chat(self):
        name = self.fake.name()
        status = 1
        update_at = self.fake.date_time_this_decade()
        return Chat(name=name, status=status, update_at=update_at)
    
    def create_fake_userchat(self, user_id, chat_id):

        return UserChat(chat_id = chat_id, user_id = user_id, message_count=0)

    def create_fake_message(self, sender_id, receiver_id, chat_id):
        text = self.fake.text()
        time_delivered = self.fake.date_time_this_decade()
        time_seen = self.fake.date_time_this_decade()
        is_delivered = self.fake.boolean()
        return Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            text=text,
            time_delivered=time_delivered,
            time_seen=time_seen,
            is_delivered=is_delivered,
            chat_id=chat_id
        )