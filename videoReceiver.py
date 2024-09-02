import cv2
import socket
import struct
import pickle


class videoReceiver:
    def __init__(self, serverIp, serverPort):
        self.__serverIp = serverIp
        self.__serverPort = serverPort
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect()
    
    def __connect(self):
        try:
            self.__client_socket.connect((self.__serverIp, self.__serverPort))
            receiveThread = threading.Thread(target=self.__receive_video)
            receiveThread.daemon = True
            receiveThread.start()
        except Exception as e:
            print(f"Client encountered an error: {e}")
        finally:
            cv2.destroyAllWindows()
            self.__client_socket.close()

    def __receive_video(self):
        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            try:
                # Receive frame size
                while len(data) < payload_size:
                    packet = self.__client_socket.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += self.__client_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow("frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except (ConnectionResetError, EOFError) as e:
                print(f"Connection error: {e}")
                break

if __name__ == "__main__":
    videoReceiver()