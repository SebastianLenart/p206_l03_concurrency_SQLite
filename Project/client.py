import json
import socket
from pprint import pprint

class Client:
    USER = "None"
    HOST = "127.0.0.1"
    PORT = 65432
    MENU = f"""uptime - return timelife of server
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
# list_of_users - only login user can see list of users
Select option: """

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect_ex((self.HOST, self.PORT))
        self.json = {"command": [],
                     "answer": "Nie rozpoznano polecenia",
                     "nick": "default",
                     "password": "",
                     "admin": "default",
                     "messages": ""}
        print(self.MENU)

    def run(self):
        while True:
            command = input(f"You are {self.json['nick']} ({self.json['admin']}), please select option: ")
            self.json["command"] = command.split(" ")
            self.sock.send(json.dumps(self.json["command"]).encode(encoding='utf8'))
            json_from_server = self.sock.recv(1024)
            self.response(json.loads(json_from_server.decode(encoding="utf8")))

    def response(self, res):
        commands = ["uptime", "info", "help"]
        self.json.update(res) # copy
        if "stop" in res["command"]:
            print("stop")
            self.sock.close()
            exit()
        elif any(res["command"] in command for command in commands):
            print(res["answer"])
            return
        elif any(res["command"] in command for command in ["login", "logout", "register"]):
            print(self.json["answer"], self.json["nick"], self.json["admin"])
        elif any(res["command"] in command for command in ["info_user", "send"]):
            print(self.json["answer"])
        elif any(res["command"] in command for command in ["show_conversation", "show_unread_texts"]):
            # pprint(self.json["answer"])
            if self.json["answer"] == "logout":
                print("logout")
                return
            print(res["command"])
            for text in self.json["answer"]:
                print(*text)
        else:
            print(res["answer"])


if __name__ == '__main__':
    client = Client()
    client.run()
