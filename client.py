import socket
from commandConstants import commandConstants
class client:

    #global variables
    FORMAT = 'utf-8'
    HEADER = 64

    def __init__(self,userName):
        self.__ip = socket.gethostbyname(socket.gethostname())
        self.__port = 5050
        self.__addr = (self.__ip, self.__port)
        self.__currentConnection = None
        self.__username = userName
        self.__friends = {}
        self.__server = None

    def getAdd(self):
        return self.__addr
    
    def send(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.__server.send(send_length)
        self.__server.send(message)

    def receive(self):
        pass
    
    def __handshake(self,addr):
        #send message to addr to ask for connection
        msg = commandConstants.REQUEST_MSG.value
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (client.HEADER - len(send_length))

    
    def connectToServer(self,addr):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.connect(addr)
        