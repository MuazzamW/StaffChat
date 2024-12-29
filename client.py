import socket
from Helpers.commandConstants import commandConstants
import threading
from Helpers.connectedManager import connectedManager
import json
import time
from GUI.clientGUI import clientGUI
class client:

    #global variables
    FORMAT = commandConstants.FORMAT.value
    HEADER = commandConstants.HEADER.value
    #input_queue = Queue()

    def __init__(self,userName):
        self.__ip = socket.gethostbyname(socket.gethostname())

        self.__username = userName
        self.__server = None
        self.__pingServer = None
        self.__connectedManager = connectedManager()
        self.__gui = None
        self.__connectToServer()
        #self.__setUpTargetListener()ping 
    
    def getAddr(self):
        return self.__ip
    
    def getServer(self):
        return self.__server

    def write(self,msg):
        if msg == commandConstants.DISCONNECT_MSG.value:
            self.__server.close()
            exit()
        message = msg.encode(client.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(client.FORMAT)
        send_length += b' ' * (client.HEADER - len(send_length))
        if msg == commandConstants.PONG_MSG.value:
            self.__pingServer.send(send_length)
            self.__pingServer.send(message)
        else:
            self.__server.send(send_length)
            self.__server.send(message)
        
    def sendUsername(self):
        self.write(f"{commandConstants.USERNAME.value}")
        self.write(f"{self.__username}")

    def __connectToServer(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #read from json file
        self.__config = json.load(open("config.json"))
        self.__serverIp = self.__config["server_ip"]
        self.__serverPort = self.__config["server_port"]
        self.__pingServerPort = self.__config["ping_server_port"]


        self.__server.connect((self.__serverIp,self.__serverPort))
        self.sendUsername()

        self.__pingServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__pingServer.connect((self.__serverIp,self.__pingServerPort))

        #start the gui
        self.__gui = clientGUI(self,self.__pingServer)
        self.__gui.run()

        self.sendUsername()
client = client(f"{input('Enter username: ')}")