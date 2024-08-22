import socket
import threading
from commandConstants import commandConstants
from connectedManager import connectedManager
from clientHandler import clientHandler
from user import User

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
            conn,addr = self.__server.accept()
             

            self.__connectedManager.addClient(User(self.__id, None, conn, addr, None))
            
            thread = clientHandler(self,conn, addr, self.__id,self.__connectedManager)
            self.__connectedManager.getClientbyID(self.__id).setThread(thread)

            print(self.__connectedManager.returnClients())
            #add the thread to the list of threads
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()}")
            self.__id += 1
            thread.daemon = True
            thread.start()

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