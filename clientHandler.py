import threading
import socket
from commandConstants import commandConstants
from connectedManager import connectedManager
class clientHandler(threading.Thread):
    def __init__(self, conn, addr, clientID, connectedManager, lock):
        super().__init__()
        self.__client_socket = conn
        self.__client_address = addr
        self.__clientID = clientID
        self.__lock = lock
        self.__connected = True
        self.__connectedManager = connectedManager
        self.__userName = self.__connectedManager.getUserName(self.__clientID) 
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
                
                match msg:
                    case commandConstants.DISCONNECT_MSG.value:
                        break
                    case commandConstants.REQUEST_MSG.value:
                        print(f"[Server: {self.__client_address}] {msg}")
                        self.sendMessage("Connection accepted")
                        self.sendMessage("Enter the IP address of the client you want to connect to")
                    case commandConstants.CLIENT_LIST_MSG.value:
                        print(f"[Server: {self.__client_address}] {msg}")
                        with self.__lock:
                            self.sendMessage(f"Connected clients: {self.__connectedManager.getConnectedClients()}")
                    case _:
                        print(f"[{self.__client_address}] {msg}")
                        self.sendMessage("Message received")
        self.__client_socket.close()
            