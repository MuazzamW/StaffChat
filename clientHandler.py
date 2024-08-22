import threading
import socket
from commandConstants import commandConstants
from connectedManager import connectedManager
import json
import queue
class clientHandler(threading.Thread):
    def __init__(self, server, conn, addr, clientID, connectedManager):
        super().__init__()
        self.__server = server
        self.__client_socket = conn
        self.__client_address = addr #tuple with ip and port
        self.__clientID = clientID
        self.__connected = True
        self.__connectedManager = connectedManager
        self.__userName = self.__connectedManager.getUserName(self.__clientID)

        print(f"[NEW CONNECTION] {self.__client_address} connected.")

        self.__ping_interval = 10  # Ping interval in seconds
        self.__ping_timeout = 5  # Ping timeout in seconds
        self.__start_ping_thread()

    def sendMessage(self, msg):
        message = msg.encode(commandConstants.FORMAT.value)
        msg_length = len(message)
        send_length = str(msg_length).encode(commandConstants.FORMAT.value)
        send_length += b' ' * (commandConstants.HEADER.value - len(send_length))  
        self.__client_socket.send(send_length)
        self.__client_socket.send(message)

    def getUserName(self):
        return self.__userName
    
    def __start_ping_thread(self):
        ping_thread = threading.Thread(target=self.__ping_client)
        ping_thread.daemon = True
        ping_thread.start()
    
    def __ping_client(self):
        while self.__connected:
            try:
                self.sendMessage("PING")
                self.__client_socket.settimeout(self.__ping_timeout)
                response = self.__client_socket.recv(commandConstants.HEADER.value).decode(commandConstants.FORMAT.value)
                if response != "PONG":
                    raise ConnectionResetError("Client did not respond to ping")
            except (ConnectionResetError, BrokenPipeError, socket.timeout):
                print(f"[DISCONNECTED] {self.__client_address} did not respond to ping.")
                self.__connected = False
                self.__client_socket.close()
                self.__connectedManager.removeClient(self.__clientID)
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                self.__connected = False
                self.__client_socket.close()
                self.__connectedManager.removeClient(self.__clientID)
                break
            finally:
                self.__client_socket.settimeout(None)
            time.sleep(self.__ping_interval) 

    def run(self):
        while self.__connected:
            try:
                self.__client_socket.settimeout(1)
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
                                target_ip = self.__client_socket.recv(msg_length).decode(commandConstants.FORMAT.value)
                                #check if client is already connected to  server
                                if self.__connectedManager.checkIfConnectedByIP(target_ip):
                                    print(f"client connected")
                                    #initiate handshake with target client
                                    self.clientConnection(target_ip)                              
                                else:
                                    #if client is not connected, then they are inactive, meaning request to connect cannot be sent
                                    self.sendMessage("Client is not connected")
                                    return
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
            except socket.timeout:
                continue
            except (ConnectionResetError, BrokenPipeError):
                print(f"[DISCONNECTED] {self.__client_address} disconnected.")
                self.__connected = False
                self.__client_socket.close()
                self.__connectedManager.removeClient(self.__clientID)
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                self.__connected = False
                self.__client_socket.close()
                self.__connectedManager.removeClient(self.__clientID)
                break
        self.__client_socket.close()

    def clientConnection(self, target_ip):
        
        client_info = json.dumps({
            "address": self.__client_address,
            "username": self.__userName,
            "message" : f"Client {self.__userName} would like to initate connection"
        })

        self.__server.clientRequest(self.__client_address, target_ip, client_info)
    
    def sendClientMsg(self, msg):
        return self.sendMessage(msg)
