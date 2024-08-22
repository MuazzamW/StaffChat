import socket
from commandConstants import commandConstants
import threading
from connectedManager import connectedManager
import json
from inputThread import inputThread
import queue
class client:

    #global variables
    FORMAT = commandConstants.FORMAT.value
    HEADER = commandConstants.HEADER.value
    #input_queue = Queue()

    def __init__(self,userName):
        self.__ip = socket.gethostbyname(socket.gethostname())

        self.__currentConnection = None
        self.__username = userName
        self.__server = None
        self.__connectedManager = connectedManager()

        self.__connectToServer()
        #self.__setUpTargetListener()ping 
    
    def getAddr(self):
        return self.__ip
    
    
    def write(self,msg):
        if msg == commandConstants.DISCONNECT_MSG.value:
            self.__server.close()
            exit()
        message = msg.encode(client.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(client.FORMAT)
        send_length += b' ' * (client.HEADER - len(send_length))
        self.__server.send(send_length)
        self.__server.send(message)
        
    def sendUsername(self):
        self.write(f"{commandConstants.USERNAME.value}")
        self.write(f"{self.__username}")

    def send(self):
        while True:
            try:
                msg = input("Enter message: ")
                self.write(msg)
                if msg == commandConstants.DISCONNECT_MSG.value:
                    break
            except Exception as e:
                #print error
                print(e)
                print("An error occurred or client disconnected")
                break

    def receive(self):
        while True:
            try:
                msg_length = self.__server.recv(client.HEADER).decode(client.FORMAT)
                if msg_length:
                    msg_length = len(msg_length)
                    msg = self.__server.recv(msg_length).decode(client.FORMAT)
                    print(f"[{self.__ip}] {msg}")
                
                    match msg:
                        case commandConstants.PING_MSG.value:
                            self.write(commandConstants.PONG_MSG.value)
                        case commandConstants.REQUEST_MSG.value:
                            print("request received")
                            json_length = self.__server.recv(client.HEADER).decode(client.FORMAT)
                            if json_length:
                                json_length = int(json_length)
                                json_msg = self.__server.recv(json_length).decode(client.FORMAT)
                                # Parse the JSON string into a Python dictionary
                                request_info = json.loads(json_msg)
                                # Extract address and username from the dictionary
                                requestIP = request_info['address'][0]
                                requestUserName = request_info['username']
                                #print(f"Request IP: {requestIP}, Request Username: {requestUserName}")

                                # Now you can handle the request with the IP and username
                                self.handleRequest(requestIP, requestUserName)
                        case commandConstants.ACCEPTED.value:
                            print("Request accepted")
                            #start video and audio stream
                        case commandConstants.DENIED.value:
                            print("Request denied")
                        case _:
                            pass

            except Exception as e:
                print(e)
                print("An error occurred or client disconnected")
                break

    def handleRequest(self,requestIP,requestUserName):
        print(f"Request from {requestUserName} with IP {requestIP}")
        valid = input("Do you want to accept the request? (y/n): ")
        
        #self.__inputThread.getInput("Do you want to accept the request? (y/n): ")

        valid = True if valid == "y" else False
        print(valid)

        targetThread = self.__connectedManager.getClientbyIP(requestIP).getThread()
        #targetThread.sendClientMsg(f"{commandConstants.ACCEPTED.value} from {self.__addr}") if valid else targetThread.sendClientMsg(commandConstants.DENIED.value)

    
    def __connectToServer(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #read from json file
        config = json.load(open("config.json"))
        server_ip = config["server-config"][0]["server_host"]
        server_port = config["server-config"][0]["server_port"]


        self.__server.connect((server_ip,server_port))
        self.sendUsername()

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send)        
        send_thread.start()

        self.sendUsername()
client = client(f"{input('Enter username: ')}")