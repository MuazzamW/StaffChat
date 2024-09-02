#streamingServer is the parent class that class that the ping, audio and video server classes inherit from
import threading
import socket
from commandConstants import commandConstants
import time
import cv2 as cv

class streamingServer(threading.Thread):
    def __init__(self, port, connectedManager):
        self.port = port
        self.ip = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.connectedManager = connectedManager
    

class pingServer(streamingServer):
    def __init__(self, port, connectedManager):
        super().__init__(port, connectedManager)
    
    def sendMessage(self, conn, msg):
        message = msg.encode('utf-8')
        msg_length = len(message)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (commandConstants.HEADER.value - len(send_length))  
        conn.send(send_length)
        conn.send(message)

    def handlePing(self, conn, addr):
        #send a ping to the client every 5 seconds
        while True:
            if not self.connectedManager.checkIfConnectedByIP(addr[0]):
                continue
            try:
                self.sendMessage(conn, commandConstants.PING_MSG.value)
                conn.settimeout(15)
                
                # Receive the length of the incoming message
                msg_length = conn.recv(commandConstants.HEADER.value).decode(commandConstants.FORMAT.value)
                #print(f"Received msg_length: {msg_length}")  # Debugging statement
                
                if msg_length:
                    try:
                        msg_length = int(msg_length)
                    except ValueError:
                        print(f"Invalid msg_length received: {msg_length}")
                        continue  # Skip this iteration if msg_length is not a valid integer
                    
                    # Receive the actual message
                    response = conn.recv(msg_length).decode(commandConstants.FORMAT.value)
                    #print(f"Received response: {response}")  # Debugging statement
                    
                    if response != commandConstants.PONG_MSG.value:
                        conn.close()
                        raise ConnectionResetError("Client did not respond to ping")
                    
                    # Reset the timeout after a successful ping
                    conn.settimeout(None)
            except Exception as e:
                print(e)
                print(f"[ERROR] {addr} has disconnected from ping server.")
                break
            finally:
                time.sleep(10)
                
                

    def run(self):
        #start listening
        self.server.listen()
        print(f"[LISTENING] Ping Server is listening on {self.server.getsockname()}")
        while True:
            conn,addr = self.server.accept()
            print(f"[NEW CONNECTION] {addr} connected for pinging.")
            ping_thread = threading.Thread(target=self.handlePing, args=(conn, addr))
            ping_thread.daemon = True
            ping_thread.start()            
    
