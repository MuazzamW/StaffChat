import socket

class client:

    #global variables
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    HEADER = 64

    def __init__(self):
        self.__ip = socket.gethostbyname(socket.gethostname())
        self.__port = 5050
        self.__addr = (self.__ip, self.__port)
        self.__currentConnection = None
        self.__friends = []

    def getAdd(self):
        return self.__addr
    
    def send(self, msg):
        pass
    
    def __handshake(self,addr):
        #send message to addr to ask for connection
        msg = "request to connect"
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (client.HEADER - len(send_length))
    
    def connect(self,addr):
        self.__currentConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(self.__handshake(addr)):   
            self.__currentConnection.connect(addr)
        