import socket
import threading
from commandConstants import commandConstants
from connectedManager import connectedManager

class server:
    def __init__(self):
        self.__PORT = 5050
        self.__IP = socket.gethostbyname(socket.gethostname())
        self.__ADDR = (self.__IP, self.__PORT)
        self.__CLIENTS = {}
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(self.__ADDR)
        self.__id = 1
        self.__connectedManager = connectedManager()
    
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        #add client to client list
        self.__CLIENTS[addr] = conn
        connected = True
        while connected:
            msg_length = conn.recv(commandConstants.HEADER).decode(commandConstants.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(commandConstants.FORMAT)
                if msg == commandConstants.DISCONNECT_MSG.value:
                    connected = False
                print(f"[{addr}] {msg}")
        conn.close()

    def start(self):
        self.__server.listen()
        print(f"[LISTENING] Server is listening on {self.__SERVER}")
        while True:
            conn,addr = self.__server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            #add the thread to the list of threads
            self.__con
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")