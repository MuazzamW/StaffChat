import socket
from commandConstants import commandConstants
import threading
class client:

    #global variables
    FORMAT = commandConstants.FORMAT.value
    HEADER = commandConstants.HEADER.value

    def __init__(self,userName):
        self.__ip = socket.gethostbyname(socket.gethostname())
        self.__port = 5050
        self.requestPort = 8000
        self.__addr = (self.__ip, self.__port)
        self.__currentConnection = None
        self.__username = userName
        self.__friends = {}
        self.__server = None

        self.__connectToServer()
        #self.__setUpTargetListener()

        #self.write(self.__username)
    
    def getAddr(self):
        return self.__addr

    
    def __setUpTargetListener(self):
        self.__targetListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__targetListener.bind(self.getAddr())
        self.__targetListener.listen()
        self.__targetListenerThread = threading.Thread(target=self.__listenForTarget)
        self.__targetListenerThread.start()
    
    def __listenForTarget(self):
        while True:
            conn, addr = self.__targetListener.accept()
            print(f"Connection from {addr} has been established")
            self.__currentConnection = conn
            self.__currentConnectionThread = threading.Thread(target=self.__receiveFromTarget)
            self.__currentConnectionThread.start()
    
    def __receiveFromTarget(self):
        while True:
            try:
                msg_length = self.__currentConnection.recv(client.HEADER).decode(client.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.__currentConnection.recv(msg_length).decode(client.FORMAT)
                    print(f"[{self.__addr}] {msg}")
            except:
                print("An error occurred or client disconnected")
                break

    def write(self,msg):
        if msg == commandConstants.DISCONNECT_MSG.value:
            self.__server.close()
            exit()
        message = msg.encode(client.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(client.FORMAT)
        send_length += b' ' * (client.HEADER - len(send_length))
        self.__server.send(send_length)
        self.__server.send(message)
        
    def sendUsername(self):
        self.write(f"{commandConstants.USERNAME.value}")
        self.write(f"{self.__username}")

    def send(self):
        while True:
            try:
                msg = input("Enter message: ")
                self.write(msg)
            except:
                print("An error occurred or client disconnected")
                break

    def receive(self):
        while True:
            try:
                msg_length = self.__server.recv(client.HEADER).decode(client.FORMAT)
                if msg_length:
                    msg_length = len(msg_length)
                    msg = self.__server.recv(msg_length).decode(client.FORMAT)
                    print(f"[{self.__addr}] {msg}")
                
                    match msg:
                        case commandConstants.REQUEST_MSG.value:
                            valid = False
                            
                        case _:
                            pass

            except:
                print("An error occurred or client disconnected")
                break
    
    def handshake(self,addr):
        #send message to addr to ask for connection
        msg = commandConstants.REQUEST_MSG.value
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (client.HEADER - len(send_length))

    
    def __connectToServer(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.connect(("172.16.16.55", 5050))
        self.sendUsername()

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send)        
        send_thread.start()

        #self.send(self.__username)
client = client(f"{input('Enter username: ')}")