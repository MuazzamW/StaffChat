import cv2
import socket
import struct
import pickle


class videoSender:
    def __init__(self,ip,port):
        # Server configuration
        self.__server_ip = ip
        self.__server_port = port
        self.cap = cv2.VideoCapture(0)
        self.__connection = None

        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__server_ip, self.__server_port))
        self.__listen()
        

    def __listen(self):
        self.__server_socket.listen(1)
        print(f"Listening on {self.__server_ip}:{self.__server_port}")
        conn, addr = self.__server_socket.accept()
        self.__connection = conn
        print(f"Connected to {addr}")
        self.__send_video()

    def __send_video(self):
    # Accept connection from client
        try:
            while True:
                # Capture frame-by-frame
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: failed to capture frame")
                frame = cv2.resize(frame, (640, 480))
                frame = cv2.flip(frame, 1)
                data = pickle.dumps(frame)
                #check if data is not empty
                message = struct.pack("Q",len(data)) + data
                try:
                    self.__connection.sendall(message)
                except BrokenPipeError:
                    print("Client has disconnected.")
                    break
        except Exception as e:
            print(f"Server encountered an error: {e}")
        finally:
            self.cap.release()
            self.__connection.close()
            self.__server_socket.close()

if __name__ == "__main__":
    videoSender()