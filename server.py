import socket
import threading
import json

class Server:
    def __init__(self):
        self.users = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket.settimeout(10)
        self.host = ""
        self.port = 8067
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.start()

    def handle_client(self, connection, address):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    print("No data received. Closing connection")
                    del self.users[str(address)]
                    connection.close()
                    break
                self.users[str(address)] = data.decode("utf-8")
                print(self.users)
                game_state = json.dumps(self.users)
                connection.send(game_state.encode("utf-8"))
            except:
                del self.users[str(address)]
                break

    def start(self):
        print("Server is running")
        while True:
            conn, addr = self.socket.accept()
            print(f"Connected by {addr}")
            self.users[str(addr)] = {}
            #print(self.users)
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr,))
            client_thread.start()



test = Server()
