import socket
import threading
from commandConstants import commandConstants
from connectedManager import connectedManager
from clientHandler import clientHandler
from user import User
import time

class server:
    def __init__(self):
        self.__PORT = 5050
        self.__IP = socket.gethostbyname(socket.gethostname())
        self.__ADDR = (self.__IP, self.__PORT)
        self.__CLIENTS = {}
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(self.__ADDR)
        self.__id = 1
        self.__connectedManager = connectedManager()

    def start(self):
        self.__server.listen()
        print(f"[LISTENING] Server is listening on {self.__server.getsockname()}")
        while True:
            conn, addr = self.__server.accept()
            user = User(self.__id, None, conn, addr, None)
            self.__connectedManager.addClient(user)
            client_handler = clientHandler(self.__server, conn, addr, self.__id, self.__connectedManager)
            client_thread = threading.Thread(target=client_handler.run)
            client_thread.start()
            self.__id += 1

    def sendMessage(self, client_ip, target_ip, msg):
        #send message to target by using the target thread's ip

        target_thread = self.__connectedManager.getClientbyIP(target_ip).getThread()
        target_thread.sendMessage(msg)
        

    def clientRequest(self, client_ip,target_ip,request_msg):
        #send request to target by using the target thread's ip
        self.sendMessage(client_ip, target_ip, request_msg)

        


    def stop(self):
        self.__server.close()
 
if __name__ == "__main__":
    server = server()
    server.start()