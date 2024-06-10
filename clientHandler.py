import threading
import socket

class clientHandler(threading.Thread):
    def __init__(self, conn, addr, clientID):
        super().__init__()
        self.__client_socket = conn
        self.__client_address = addr
        self.__connected = True
        print(f"[NEW CONNECTION] {self.__client_address} connected.")
    
    def run(self):
        try:
            # Receive client ID
            self.client_id = self.client_socket.recv(1024).decode()
            self.clients[self.client_id] = (self.client_socket, self.client_address)
            print(f"Client {self.client_id} connected from {self.client_address}")

            while self.__connected:
                # Receive the ID of the client to connect to
                target_id = self.client_socket.recv(1024).decode()
                if target_id in self.clients:
                    target_socket, target_addr = self.clients[target_id]
                    # Send target client address to the requesting client
                    self.client_socket.sendall(f"ADDRESS:{target_addr[0]}:{target_addr[1]}".encode())
                    # Send requesting client address to the target client
                    target_socket.sendall(f"ADDRESS:{self.client_address[0]}:{self.client_address[1]}".encode())
                else:
                    self.client_socket.sendall(b"ERROR:Client not found")
        except:
            print(f"Client {self.client_address} disconnected")
        finally:
            self.client_socket.close()
            if self.client_id in self.clients:
                del self.clients[self.client_id]