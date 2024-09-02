import cv2
import socket
import struct
import pickle

# Client configuration
SERVER_IP = 'localhost'
SERVER_PORT = 9090

# Create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_IP, SERVER_PORT))

    while True:
        try:
            # Receive frame size
            data = client_socket.recv(struct.calcsize("L"))
            if not data:
                break
            frame_size = struct.unpack("L", data)[0]

            # Receive frame data
            data = b''
            while len(data) < frame_size:
                packet = client_socket.recv(frame_size - len(data))
                if not packet:
                    break
                data += packet

            # Deserialize frame
            frame = pickle.loads(data)

            # Display frame
            cv2.imshow('Received Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except (ConnectionResetError, EOFError) as e:
            print(f"Connection error: {e}")
            break
except Exception as e:
    print(f"Client encountered an error: {e}")
finally:
    cv2.destroyAllWindows()
    client_socket.close()