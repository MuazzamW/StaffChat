import socket

class client:

    #global variables
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"

    def __init__(self):
        self.__ip = socket.gethostbyname(socket.gethostname())
        self.__port = 5050
        self.__addr = (self.__ip, self.__port)

    def send(self, msg):
        pass