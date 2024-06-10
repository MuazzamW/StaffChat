import threading
import socket
from commandConstants import commandConstants
class clientHandler(threading.Thread):
    def __init__(self, conn, addr, clientID):
        super().__init__()
        self.__client_socket = conn
        self.__client_address = addr
        self.__clientID = clientID
        self.__connected = True
        print(f"[NEW CONNECTION] {self.__client_address} connected.")
    
    
    def sendMessage(self, msg):
        message = msg.encode(commandConstants.FORMAT.value)
        msg_length = len(message)
        send_length = str(msg_length).encode(commandConstants.FORMAT.value)
        send_length += b' ' * (commandConstants.HEADER.value - len(send_length))
        self.__client_socket.send(send_length)
        self.__client_socket.send(message)

    def run(self):
        while True:
            msg_length = self.__client_socket.recv(commandConstants.HEADER.value).decode(commandConstants.FORMAT.value)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.__client_socket.recv(msg_length).decode(commandConstants.FORMAT.value)
                if msg == commandConstants.DISCONNECT_MSG.value:
                    self.__connected = False
                    break
                elif msg == commandConstants.REQUEST_MSG.value:
                    print(f"[{self.__client_address}] {msg}")
                    self.sendMessage("Connection accepted")
                else:
                    print(f"[{self.__client_address}] {msg}")
                    self.sendMessage("Message received")
            