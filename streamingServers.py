#streamingServer is the parent class that class that the ping, audio and video server classes inherit from
import threading
import socket

class streamingServer(threading.Thread):
    def __init__(self, port):
        self.__port = port
        self.__ip = socket.gethostbyname(socket.gethostname())
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((self.__ip, self.__port))
    

class pingServer(streamingServer):
    def __init__(self, port):
        super().__init__(port)
    
    def sendMessage(self, conn, msg):
        message = msg.encode('utf-8')
        msg_length = len(message)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (1024 - len(send_length))  
        conn.send(send_length)
        conn.send(message)

    def run(self):
        self.__server.listen()
        print(f"[LISTENING] Server is listening on {self.__server.getsockname()}")
        while True:
            conn,addr = self.__server.accept()
            print(f"[NEW CONNECTION] {addr} connected.")
            conn.send("Pong".encode('utf-8'))
            conn.close()
    
                          