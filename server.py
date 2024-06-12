import socket
import threading
from commandConstants import commandConstants
from connectedManager import connectedManager
from clientHandler import clientHandler
from user import User

class server:
    def __init__(self):
        self.__PORT = 5050
        self.__IP = socket.gethostbyname("localhost")
        self.__ADDR = (self.__IP, self.__PORT)
        self.__CLIENTS = {}
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(self.__ADDR)
        self.__id = 1
        self.__connectedManager = connectedManager()
        self.lock = threading.Lock()

    def start(self):
        self.__server.listen()
        print(f"[LISTENING] Server is listening on {self.__server.getsockname()}")
        while True:
            conn,addr = self.__server.accept()
            #receive username
            #thread = threading.Thread(target=self.handle_client, args=(conn, addr))
             
            with self.lock:
                self.__connectedManager.addClient(User(self.__id, None, conn, addr, None))
            
            thread = clientHandler(conn, addr, self.__id,self.__connectedManager,self.lock)
            self.__connectedManager.getClient(self.__id).setThread(thread)

            print(self.__connectedManager.returnClients())
            #add the thread to the list of threads
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
            self.__id += 1
            thread.start()
            

    def stop(self):
        self.__server.close()

if __name__ == "__main__":
    server = server()
    server.start()