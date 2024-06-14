import threading
import socket
from commandConstants import commandConstants
from connectedManager import connectedManager
from  multipledispatch import dispatch
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
    
    @dispatch(str)
    def sendMessage(self, msg):
        message = msg.encode(commandConstants.FORMAT.value)
        msg_length = len(message)
        send_length = str(msg_length).encode(commandConstants.FORMAT.value)
        send_length += b' ' * (commandConstants.HEADER.value - len(send_length))
        self.__client_socket.send(send_length)
        self.__client_socket.send(message)
    
    @dispatch(str, socket.socket)
    def sendMessage(self, msg, clientSocket):
        print("entered sendMessage 2")
        message = msg.encode(commandConstants.FORMAT.value)
        msg_length = len(message)
        send_length = str(msg_length).encode(commandConstants.FORMAT.value)
        send_length += b' ' * (commandConstants.HEADER.value - len(send_length))
        clientSocket.send(send_length)
        clientSocket.send(message)

    def run(self):
        while True:
            try:
                msg_length = self.__client_socket.recv(commandConstants.HEADER.value).decode(commandConstants.FORMAT.value)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.__client_socket.recv(msg_length).decode(commandConstants.FORMAT.value)
                    print(f"[Server: {self.__client_address}] {msg}")
                    match msg:
                        case commandConstants.DISCONNECT_MSG.value:
                            break
                        case commandConstants.REQUEST_MSG.value:   
                            self.sendMessage("Enter the IP address of the client you want to connect to")
                            msg_length = self.__client_socket.recv(commandConstants.HEADER.value).decode(commandConstants.FORMAT.value)
                            if msg_length:
                                msg_length = int(msg_length)
                                client_ip = self.__client_socket.recv(msg_length).decode(commandConstants.FORMAT.value)
                                client_port = 6000
                                self.clientConnection(client_ip, client_port)
                            self.clientConnection(client_ip, client_port)
                        case commandConstants.CLIENT_LIST_MSG.value:
                            self.sendMessage(f"Connected clients: {self.__connectedManager.returnClients()}")
                        case commandConstants.USERNAME.value:
                            msg_length = self.__client_socket.recv(commandConstants.HEADER.value).decode(commandConstants.FORMAT.value)
                            if msg_length:
                                msg_length = int(msg_length)
                                self.__userName = self.__client_socket.recv(msg_length).decode(commandConstants.FORMAT.value)
                            self.__connectedManager.getClientbyID(self.__clientID).setUserName(self.__userName)
                            self.sendMessage(f"Username set to {self.__userName}")
                        case _:
                            self.sendMessage("Message received")
            except Exception as e:
                print(f"[ERROR] {e.with_traceback(None)}")
                print(f"[DISCONNECTED] {self.__client_address} disconnected.")
                self.__connectedManager.removeClient(self.__clientID)
                break
        self.__client_socket.close()


    def clientConnection(self, clientIP, clientPort):
        
        #check if client is already connected to server
        if self.__connectedManager.checkIfConnectedByIP(clientIP):
            print(f"client connected")
            targetThread = self.__connectedManager.getClientbyIP(clientIP).getThread()
            targetThread.sendClientMsg(f"{commandConstants.REQUEST_MSG.value} from {self.__userName}:{self.__client_address}")
            #if client is connected, then they are active, meaning request to connect can be sent
        else:
            #if client is not connected, then they are inactive, meaning request to connect cannot be sent
            self.sendMessage("Client is not connected")
            return
    
    def sendClientMsg(self, msg):
        return self.sendMessage(msg)
