
import unittest
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from main import MessagesRepository, UserRepository, ChatRepository, UserChatRepository
from FakeDataGenerator import FakeDataGenerator

fake = Faker()

class TestUsersRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('postgresql://postgres:123@localhost/chat')
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()

        self.messages_repository = MessagesRepository(self.db_session)
        self.user_repository = UserRepository(self.db_session)
        self.chat_repository = ChatRepository(self.db_session)

    def tearDown(self):
        self.db_session.rollback()
        self.db_session.close()

    def test_get_user_by_id(self):
        fake_data_generator = FakeDataGenerator()

        new_user = fake_data_generator.create_fake_user()
        self.user_repository.create(new_user)

        response = self.user_repository.get_user_by_id(user_id=new_user.id)
        self.assertIsNotNone(response)
        self.assertEqual(response.id, new_user.id)

    def test_get_chats_with_user(self):
        fake_data_generator = FakeDataGenerator()

        new_user = fake_data_generator.create_fake_user()
        self.user_repository.create(new_user)

        newchat = fake_data_generator.create_fake_chat()
        self.chat_repository.create(newchat)

        response = self.user_repository.get_chats_with_user(user_id=new_user.id, status=newchat.status)

        for chat in response.chats:
            self.assertEqual(chat.user_id, new_user.id)



class TestMessagesRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('postgresql://postgres:123@localhost/chat')
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()

        self.messages_repository = MessagesRepository(self.db_session)
        self.user_repository = UserRepository(self.db_session)
        self.chat_repository = ChatRepository(self.db_session)

    def tearDown(self):
        self.db_session.rollback()
        self.db_session.close()

    def test_get_messages_with_sender_id(self):
        fake_data_generator = FakeDataGenerator()

        sender_user = fake_data_generator.create_fake_user()
        self.user_repository.create(sender_user)

        receiver_user = fake_data_generator.create_fake_user()
        self.user_repository.create(receiver_user)

        newchat = fake_data_generator.create_fake_chat()
        self.chat_repository.create(newchat)

        message = fake_data_generator.create_fake_message(sender_user.id, receiver_user.id, newchat.id)
        self.messages_repository.create(message)

        response = self.messages_repository.get_messages(sender_id=sender_user.id)

        self.assertTrue(len(response) > 0)
        for msg in response:
            self.assertEqual(msg.sender_id, sender_user.id)

    def test_get_messages_with_receiver_id(self):
        fake_data_generator = FakeDataGenerator()

        sender_user = fake_data_generator.create_fake_user()
        self.user_repository.create(sender_user)

        receiver_user = fake_data_generator.create_fake_user()
        self.user_repository.create(receiver_user)

        newchat = fake_data_generator.create_fake_chat()
        self.chat_repository.create(newchat)

        message = fake_data_generator.create_fake_message(sender_user.id, receiver_user.id, newchat.id)
        self.messages_repository.create(message)

        response = self.messages_repository.get_messages(receiver_id=receiver_user.id)

        self.assertTrue(len(response) > 0)
        for msg in response:
            self.assertEqual(msg.receiver_id, receiver_user.id)

    def test_get_messages_with_senderId_receiverId_timeDelivered(self):
        fake_data_generator = FakeDataGenerator()

        sender_user = fake_data_generator.create_fake_user()
        self.user_repository.create(sender_user)

        receiver_user = fake_data_generator.create_fake_user()
        self.user_repository.create(receiver_user)

        newchat = fake_data_generator.create_fake_chat()
        self.chat_repository.create(newchat)

        message = fake_data_generator.create_fake_message(sender_user.id, receiver_user.id, newchat.id)
        self.messages_repository.create(message)

        response = self.messages_repository.get_messages(sender_id=sender_user.id, receiver_id=receiver_user.id, time_delivered=message.time_delivered)

        self.assertTrue(len(response) > 0)
        for msg in response:
            self.assertEqual(msg.receiver_id, receiver_user.id)
            self.assertEqual(msg.sender_id, sender_user.id)
            self.assertEqual(msg.time_delivered, message.time_delivered)

class TestChatRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('postgresql://postgres:123@localhost/chat')
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()

        self.messages_repository = MessagesRepository(self.db_session)
        self.user_repository = UserRepository(self.db_session)
        self.chat_repository = ChatRepository(self.db_session)
        self.userchat_repository = UserChatRepository(self.db_session)

    def tearDown(self):
        self.db_session.rollback()
        self.db_session.close()

    def test_get_total_chat_count_for_users(self):
        fake_data_generator = FakeDataGenerator()

        sender_user = fake_data_generator.create_fake_user()
        self.user_repository.create(sender_user)

        receiver_user = fake_data_generator.create_fake_user()
        self.user_repository.create(receiver_user)
        
        chat1 = fake_data_generator.create_fake_chat()
        self.chat_repository.create(chat1)
        userchat1 = fake_data_generator.create_fake_userchat(sender_user.id, chat1.id)
        self.userchat_repository.create(userchat1)

        userchat2 = fake_data_generator.create_fake_userchat(sender_user.id, chat1.id)
        self.userchat_repository.create(userchat2)

        response = self.chat_repository.get_total_chat_count_for_users(user_id1=sender_user.id, user_id2=receiver_user.id)
        expected_chats_count = 1

        if response != response:
            raise AssertionError(f"Expected {expected_chats_count} chats, but got {response}")




class TestUserChatRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('postgresql://postgres:123@localhost/chat')
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()

        self.messages_repository = MessagesRepository(self.db_session)
        self.user_repository = UserRepository(self.db_session)
        self.chat_repository = ChatRepository(self.db_session)
        self.userchat_repository = UserChatRepository(self.db_session)

    def tearDown(self):
        self.db_session.rollback()
        self.db_session.close()

    def test_get_total_message_count(self):
        fake_data_generator = FakeDataGenerator()

        sender_user = fake_data_generator.create_fake_user()
        self.user_repository.create(sender_user)

        receiver_user = fake_data_generator.create_fake_user()
        self.user_repository.create(receiver_user)

        newchat = fake_data_generator.create_fake_chat()
        self.chat_repository.create(newchat)

        userchat1 = fake_data_generator.create_fake_userchat(user_id=sender_user.id, chat_id=newchat.id)
        self.userchat_repository.create(userchat1)

        message = fake_data_generator.create_fake_message(sender_user.id, receiver_user.id, newchat.id)
        self.messages_repository.create(message)

        response = self.userchat_repository.get_total_message_count(chat_id=newchat.id)
        expected_message_count = userchat1.message_count

        if response != expected_message_count:
            raise AssertionError(f"Expected {expected_message_count} messages, but got {response}")
        

