import json
import datetime
import socket
from user_sql import User
from connection_pool import ConnectionPool
from threading import Thread


class Serwer:
    HOST = "127.0.0.1"
    PORT = 65432
    HELP = f"""uptime - return timelife of server
info - return version and date of create server
help - return described options, just like that     
stop - stop server and client
login <nick> <password> - let you login to system
logout - let you logout from system
register <nick> <password> <admin>- only admin can add new user
info_user <nick> - only admin can see info about everybody
send <nick> <message> - only register user can send message to receiver
show_conversation <nick> - only login user see conversation
show_unread_texts - only login user see unread texts
list of users - only login user can see list of users
"""

    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.date_of_create = self.start_time.strftime("%d/%m/%Y")
        print(self.date_of_create)
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lsock.bind((self.HOST, self.PORT))
        self.lsock.listen()
        print(f"Listening on {(self.HOST, self.PORT)}")
        self.stopFlag = False
        self.answer_to_send = {"command": "Nie rozpoznano polecenia",
                               "answer": "",
                               "nick": "default",
                               "password": "",
                               "admin": "default",
                               "messages": ""}
        self.connection_db = ConnectionPool()
        self.user = User(self.connection_db)
        self.list_of_current_login_users = []
        self.check_connections_db()

    def check_connections_db(self):
        check_connections = Thread(target=self.connection_db.check_amount_of_conections, daemon=True)
        check_connections.start()

    def run(self):
        conn, addr = self.lsock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")

        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                sdata = json.loads(data.decode(encoding="utf8"))
                if not sdata:
                    break
                self.options(sdata, conn)
                if self.stopFlag:
                    break

    def options(self, data, conn):
        dict_options = {
            "uptime": self.uptime,
            "info": self.info,
            "help": self.help,
            "stop": self.stop,
            "login": lambda nick, password: self.login(nick, password),
            "logout": self.logout,
            "register": lambda nick, password, admin: self.register(nick, password, admin),
            "info_user": lambda nick: self.info_user(nick),
            "send": lambda nick, *message: self.send_text_to(nick, message),
            "show_conversation": lambda nick: self.show_conversation(nick),
            "show_unread_texts": self.show_unread_texts
        }
        try:
            dict_options[data[0]](*data[1:])
        except KeyError:
            self.default_answer()
            print("KeyError")
        except TypeError:
            self.default_answer()
            self.answer_to_send["answer"] = "Za malo przekazanych argumetow"
            print("TypeError", data)
        self.answer_to_send["command"] = data[0]
        self.answer_to_send = json.dumps(self.answer_to_send).encode(encoding='utf8')
        conn.sendall(self.answer_to_send)
        self.default_answer()

        if self.stopFlag:
            self.lsock.close()

    def default_answer(self):
        self.answer_to_send = {"command": "Nie rozpoznano polecenia",
                               "answer": "Nie rozpoznano polecenia",
                               # "nick": "default",
                               "password": "",
                               # "admin": "default",
                               "messages": ""}

    def uptime(self):
        answer = str(datetime.datetime.now() - self.start_time)[:7]
        self.answer_to_send["answer"] = answer  # na zalogowanym Sebie wywala mi tutaj błąd !!!!!
        print(self.answer_to_send["answer"])

    def info(self):
        answer = f"Version: {'1.0.0'}, date of create server: {self.date_of_create}"
        self.answer_to_send["answer"] = answer
        print(self.answer_to_send["answer"])

    def help(self):
        answer = self.HELP
        self.answer_to_send["answer"] = answer
        print(self.answer_to_send["answer"])

    def stop(self):
        answer = "stop"
        self.answer_to_send["answer"] = answer
        self.stopFlag = True
        print(self.answer_to_send["answer"])

    def login(self, nick="default", password="default"):
        self.answer_to_send["answer"] = self.user.login(nick, password)
        self.answer_to_send["nick"] = self.user.nick
        # self.answer_to_send["password"] = self.user.password
        self.answer_to_send["admin"] = self.user.admin
        print("Login " + self.answer_to_send["answer"])

    def logout(self):
        del self.user
        self.user = User()
        self.answer_to_send = {"command": "Nie rozpoznano polecenia", "answer": "logout", "nick": "default",
                               "password": "", "admin": "default", "messages": ""}
        print("Logout")

    def register(self, nick, password, admin):
        self.answer_to_send["answer"] = self.user.register_new_user(nick, password, admin)
        # self.answer_to_send["nick"] = "default"
        # self.answer_to_send["admin"] = "default"
        # print("Register done") # nieprawda bo jak nie bedzie admina to tez sie wyswietli..trzeba ifa dac

    def info_user(self, nick):
        self.answer_to_send["answer"] = self.user.show_base_info_about(nick)

    def send_text_to(self, nick, message):
        # check user is login:
        if self.current_login():
            return
        text = [str(datetime.datetime.now()), "".join(map(lambda x: x + " ", message))]
        self.answer_to_send["answer"] = self.user.send_text_to(nick, text)

    def show_conversation(self, nick):
        if self.current_login():
            return
        self.answer_to_send["answer"] = self.user.show_conversation(nick)

    def show_unread_texts(self):
        if self.current_login():
            return
        self.answer_to_send["answer"] = self.user.read_unread_messages()

    def current_login(self):
        if self.user.nick is None:
            self.default_answer()
            self.answer_to_send["answer"] = "logout"
            return True
        self.answer_to_send["nick"] = self.user.nick
        self.answer_to_send["admin"] = self.user.admin
        return False


if __name__ == '__main__':
    server = Serwer()
    server.run()
