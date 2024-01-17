from connect_sql import GetConnection
import database_sqlite
import json
from pprint import pprint
import datetime
from connection_pool import ConnectionPool, TooMuchConnections


class User:
    BUFOR_MESSAGES = 5

    def __init__(self, connection_db):
        self.nick = None
        self.password = None
        self.admin = None
        self.messages = None
        self.users_file = None
        self.connection_db = connection_db.get_connection() # qlbo przy kazej funkcji indywidualnie

    # add to new user can only admin
    def register_new_user(self, nick="Default", password="1234", admin=False):
        try:
            if not self.admin:
                print(f"Only admin can add new user!")
                return f"Only admin can add new user!"
            for user in database_sqlite.get_list_nicks(self.connection_db):
                if user[0] == nick:
                    return f"This nick is busy."
            new_user = {
                "nick": nick,
                "password": password,
                "admin": admin
            }
            return_value = database_sqlite.add_new_user(self.connection_db, **new_user)
            pprint(return_value)
            return f"Register done!"
        except TooMuchConnections:
            print("To much connections")
            return "To much connections"

    def show_list_users(self):
        try:
            return [element[0] for element in database_sqlite.get_list_nicks(self.connection_db)]
        except TooMuchConnections:
            print("To much connections")
            return "To much connections"

    def show_base_info_about(self, nick):
        if not self.admin:
            return f"Only admin can get info!"
        try:
            return database_sqlite.get_base_info(self.connection_db, nick)
        except TooMuchConnections:
            print("To much connections")

    def login(self, nick: str = "Default", password: str = "1234"):
        try:
            if nick not in [element[0] for element in database_sqlite.get_list_nicks(self.connection_db)]:
                return f"Not found user {nick}"
            user = database_sqlite.get_base_info(self.connection_db,
                                                 nick)  # powyzsze linijki sa zbedne przy tym zapisie..
            if user[0] == nick and user[1] == password:
                self.set_data_from_db(*user)
                return f"Login"
            return f"Password is wrong"
        except TooMuchConnections:
            print("To much connections")
            return "To much connections"

    def check_user_exists(self, nick="Olaf"):
        try:
            for user in database_sqlite.get_list_nicks(self.connection_db):
                if user[0] == nick:
                    return True
            # raise SomethingWrong(f"Not found user {nick}")
            return False
        except TooMuchConnections:
            print("To much connections")
            return "To much connections"

    def set_data_from_db(self, nick="default", password="default", admin="False"):
        self.nick = nick
        self.password = password
        self.admin = admin

    def show_conversation(self, nick="Olaf"):
        if not self.check_do_u_have_this_nick_in_conversation(nick):
            print("You dont have this nick in conversation")
            return
        self.check_unread_messages()
        self.read_unread_messages()
        sorted_messages = self.sort_messages_by_date(nick)
        print(f"Conversation with {nick}:")
        if len(sorted_messages) == 0:
            print("- Empty")
        only_text = list(map(lambda x: x[3], sorted_messages))
        # pprint(only_text)
        sorted_messagesv2 = sorted(sorted_messages, key=lambda x: x[4])
        pprint(sorted_messagesv2)
        return sorted_messagesv2

    def sort_messages_by_date(self, from_nick="Olaf"):
        try:
            messages_from_sb = database_sqlite.get_conversation_by_nick(self.connection_db, self.nick, from_nick)
            # messages_from_sb_sort_reverse = sorted(messages_from_sb, key=lambda x: x[4], reverse=True)
            # pprint(messages_from_sb_sort_reverse)
            return messages_from_sb
        except TooMuchConnections:
            print("To much connections")
            return "To much connections"

    def check_unread_messages(self):
        try:
            counter_unread = database_sqlite.get_counter_unread_messages(
                self.connection_db, self.nick)
            if len(counter_unread) == 0:
                return []
            for unread in counter_unread:
                print(f"You {unread[0]} have {unread[2]} messages from {unread[1]}")
            return counter_unread
        except TooMuchConnections:
            print("To much connections")
            return "To much connections"

    def read_unread_messages(self):
        try:
            unread_messages = database_sqlite.get_unread_messages(self.connection_db)
            unread_messages3 = []
            for text in unread_messages:
                print(f"{text[0]} have unread message(s) from {text[3]}: {text[4]}")
                database_sqlite.update_unread_message(self.connection_db, text[2])
                unread_messages3.append(tuple([text[0], "from", text[3], text[4]]))
            unread_messages2 = list(map(lambda x: x[0], unread_messages))
            if len(unread_messages) == 0:
                return ["You dont have unread texts"]
            return unread_messages3
        except TooMuchConnections:
            print("To much connections")
            return "To much connections"

    def check_bufor_in_receiver(self, nick="Olaf"):
        try:
            try:
                counter_unread_messages = database_sqlite.get_counter_unread_messages_with_sb(self.connection_db,
                                                                                              self.nick, nick)
                print(counter_unread_messages[2])
            except IndexError:
                counter_unread_messages = 0
            if counter_unread_messages >= self.BUFOR_MESSAGES:
                return True
            return False
        except TooMuchConnections:
            print("To much connections")
            return "To much connections"

    def send_text_to(self, send_to_nick="Olaf", text: list = [str(datetime.datetime.now()), "sth"]):
        if not self.check_user_exists(send_to_nick):
            return f"Not found user {send_to_nick}"  # niemożemy wyslac do osoby ktora nie istnieje
        if self.check_bufor_in_receiver(send_to_nick):
            return f"Bufor is full, you cant sent text"

        try:
            sender_or_receiver = database_sqlite.determine_sender_or_receiver(self.connection_db)[0]
            text.insert(0, f"{sender_or_receiver[1]}")
            if not self.check_do_u_have_this_nick_in_conversation(send_to_nick):
                print("You dont have this nick in conversation, Now it's going to be added")
                print(database_sqlite.add_conversation(self.connection_db, self.nick, send_to_nick))
            id_conversation = database_sqlite.get_id_conversation(self.connection_db, self.nick, send_to_nick)
            print("id_message", database_sqlite.add_message(self.connection_db, text[:], id_conversation))
            return f"Send ok"
        except TooMuchConnections:
            print("To much connections")
            return "To much connections"

    def check_do_u_have_this_nick_in_conversation(self, nick="Olaf"):
        try:
            list_users = database_sqlite.get_nicks_conversation(self.connection_db,
                                                                self.nick)  # dodaj self.nick ale dopiero po zalogowaniu!!!
            for user in list_users:
                if nick == user[0]:
                    return True
            return False
        except TooMuchConnections:
            print("To much connections")
            return "To much connections"



if __name__ == '__main__':
    user = User()
    pprint(user.read_unread_messages())

"""
if __name__ == '__main__':  # !!! bez tego ponizsze linijki beda wywolywane gdy gdzies uzyjemy 'from user import User'
    user = User()
    print(user.login("Seba", "qaz123"))
    # print(user.login("Olaf", "qaz321"))
    # user.check_unread_messages()
    # user.send_text_to("Olaf", ["wiadomosc", "17"])
    # user.show_conversation("Olaf")

"""
