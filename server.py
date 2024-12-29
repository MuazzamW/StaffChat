import json
import socket
import threading
from Helpers.connectedManager import connectedManager
from Helpers.clientHandler import clientHandler
from Helpers.user import User
from server.streamingServers import pingServer

class server:
    def __init__(self):
        #read port from config.json
        self.__config = json.load(open("config.json"))
        self.__PORT = self.__config["server_port"]
        print(self.__PORT)
        self.__IP = socket.gethostbyname(socket.gethostname())
        self.__ADDR = (self.__IP, self.__PORT)
        self.__CLIENTS = {}
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(self.__ADDR)
        self.__id = 1
        self.__connectedManager = connectedManager()
        self.__pingServer = pingServer(self.__config["ping_server_port"], self.__connectedManager)

    def start(self):
        #start ping server on a separate thread
        ping_thread = threading.Thread(target=self.__pingServer.run)
        ping_thread.daemon = True
        ping_thread.start()

        self.__server.listen()
        print(f"[LISTENING] Server is listening on {self.__server.getsockname()}")
        while True:
            conn, addr = self.__server.accept()
            user = User(self.__id, None, conn, addr, None)
            self.__connectedManager.addClient(user)
            client_handler = clientHandler(self.__server, conn, addr, self.__id, self.__connectedManager)
            client_thread = threading.Thread(target=client_handler.run)
            #set the thread in the user object
            user.setThread(client_handler)
            client_thread.start()

             
            self.__id += 1

            #check if any clients are still connected
            if self.__connectedManager.returnClients() == {}:
                print("No clients connected")
                self.stop()


    def stop(self):
        self.__server.close()
 
if __name__ == "__main__":
    server = server()
    server.start()