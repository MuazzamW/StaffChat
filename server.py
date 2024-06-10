import socket
import threading
from commandConstants import commandConstants
from connectedManager import connectedManager
from clientHandler import clientHandler
from user import User

class server:
    def __init__(self):
        self.__PORT = 5050
        self.__IP = socket.gethostbyname(socket.gethostname())
        self.__ADDR = (self.__IP, self.__PORT)
        self.__CLIENTS = {}
        self.__threads = {}
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(self.__ADDR)
        self.__id = 1
        self.__connectedManager = connectedManager()

    def start(self):
        self.__server.listen()
        print(f"[LISTENING] Server is listening on {self.__server.getsockname()}")
        while True:
            conn,addr = self.__server.accept()
            #thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread = clientHandler(conn, addr, self.__id) 
            #add the thread to the list of threads
            self.__CLIENTS[self.__id] = User(self.__id, thread)
            thread.run()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            self.__id += 1

    def stop(self):
        self.__server.close()

if __name__ == "__main__":
    server = server()
    server.start()