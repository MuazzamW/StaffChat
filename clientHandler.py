import threading
import socket
from commandConstants import commandConstants
from connectedManager import connectedManager
import json
import time
from videoReceiver import videoReceiver
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
        self.__waiting_response = False
        self.__originalThread = None

        print(f"[NEW CONNECTION] {self.__client_address} connected.")

    def getClientIp(self):
        return self.__client_address[0]

    def sendMessage(self, msg, originalThread = None, request = False):
        self.__originalThread = originalThread
        message = msg.encode(commandConstants.FORMAT.value)
        msg_length = len(message)
        send_length = str(msg_length).encode(commandConstants.FORMAT.value)
        send_length += b' ' * (commandConstants.HEADER.value - len(send_length))
        if request:
            self.__waiting_response = True
            self.__client_socket.send(send_length)
            self.__client_socket.send(message)
        else:  
            self.__client_socket.send(send_length)
            self.__client_socket.send(message)

    def getUserName(self):
        return self.__userName

    def run(self):
        waiting_for_username = False
        while self.__connected:
            try:
                self.__client_socket.settimeout(1)
                msg_length = self.__client_socket.recv(commandConstants.HEADER.value).decode(commandConstants.FORMAT.value)
                if not waiting_for_username:
                    if not self.__waiting_response:
                        if msg_length:
                            msg_length = int(msg_length)
                            msg = self.__client_socket.recv(msg_length).decode(commandConstants.FORMAT.value)
                            print(f"[Server: {self.__client_address}] {msg}")
                            match msg:
                                case commandConstants.DISCONNECT_MSG.value:
                                    break
                                case commandConstants.REQUEST_MSG.value:   
                                    self.sendMessage("Enter the user name of the client you want to connect to")
                                    waiting_for_username = True
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
                    else:
                        waiting_response = False
                        if msg_length:
                            msg_length = int(msg_length)
                            response = self.__client_socket.recv(msg_length).decode(commandConstants.FORMAT.value)
                            msg = f"{self.__userName} has accepted your request" if response == commandConstants.ACCEPTED.value else f"{self.__userName} has denied your request"
                            self.__originalThread.sendMessage(msg)
                            self.__originalThread.sendMessage(commandConstants.ACCEPTED.value if response == commandConstants.ACCEPTED.value else commandConstants.DENIED.value)
                            if response == commandConstants.ACCEPTED.value:
                                #wait 3 seconds for videoreceiver to start
                                time.sleep(3)
                                videoReceiver(self.__originalThread.getClientIP(),8080)

                            
                else:
                    # Wait for the client to send the username
                    print(f"msg_length: {msg_length}")  # Debugging statement  
                    if msg_length:
                        msg_length = int(msg_length)
                        userName = self.__client_socket.recv(msg_length).decode(commandConstants.FORMAT.value)
                        # Check if client is already connected to server
                        if self.__connectedManager.checkIfConnectedByUserName(userName):
                            print(f"client connected")
                            # Initiate handshake with target client
                            self.clientConnection(userName)
                        else:
                            # If client is not connected, then they are inactive, meaning request to connect cannot be sent
                            self.sendMessage("Client is not connected or inactive.")
                        waiting_for_username = False  # Reset flag to continue the loop
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

    def clientConnection(self, userName):
        
        client_info = json.dumps({
            "address": self.__client_address,
            "username": self.__userName,
            "message" : f"Client {self.__userName} would like to initate connection, do you accept? (type !ACCEPT or !DENY)"
        })

        print(f"Client info: {client_info}")
        
        #find the target thread
        target_thread = self.__connectedManager.getClientbyUserName(userName).getThread()
        print(f"target thread is {target_thread}")
        #send only the message from client_info to the target client
        target_thread.sendMessage(client_info, self,request=True)   
        
        

    
    def sendClientMsg(self, msg):
        return self.sendMessage(msg)
