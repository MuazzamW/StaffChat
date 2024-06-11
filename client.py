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
        self.__addr = (self.__ip, self.__port)
        self.__currentConnection = None
        self.__username = userName
        self.__friends = {}
        self.__server = None

        self.__connectToServer()

        #self.write(self.__username)
    
    def getAddr(self):
        return self.__addr
    
    def write(self,msg):
        message = msg.encode(client.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(client.FORMAT)
        send_length += b' ' * (client.HEADER - len(send_length))
        self.__server.send(send_length)
        self.__server.send(message)


    def send(self):
        while True:
            try:
                msg = input("Enter message: ")
                self.write(msg)
            except:
                self.__connectToServer()
                continue

    def receive(self):
        while True:
            msg_length = self.__server.recv(client.HEADER).decode(client.FORMAT)
            if msg_length:
                msg_length = len(msg_length)
                msg = self.__server.recv(msg_length).decode(client.FORMAT)
                print(f"[{self.__addr}] {msg}")
    
    def handshake(self,addr):
        #send message to addr to ask for connection
        msg = commandConstants.REQUEST_MSG.value
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (client.HEADER - len(send_length))

    
    def __connectToServer(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.connect(self.__addr)

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send)        
        send_thread.start()

        #self.send(self.__username)
client = client(f"{input('Enter username: ')}")