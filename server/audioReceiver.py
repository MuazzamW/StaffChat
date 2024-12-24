import pyaudio
import socket

class audioReceiver:
    def __init__(self, serverIp, serverPort):
        self.__FORMAT = pyaudio.paInt16
        self.__CHANNELS = 1
        self.__RATE = 44100
        self.__CHUNK = 1024
        self.__serverIp = serverIp
        self.__serverPort = serverPort

        print("Audio Receiver started")
        #self.receive_audio()

    def receive_audio(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.__serverIp, self.__serverPort))
        print(f"Connected to server at {self.__serverIp}:{self.__serverPort}")

        # Initialize audio stream
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.__FORMAT,
                            channels=self.__CHANNELS,
                            rate=self.__RATE, 
                            output=True, 
                            frames_per_buffer=self.__CHUNK)

        try:
            while True:
                # Receive audio data from the server
                data = client_socket.recv(self.__CHUNK)
                if not data:
                    break
                # Play audio data
                stream.write(data)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Cleanup
            stream.stop_stream()
            stream.close()
            audio.terminate()
            client_socket.close()

if __name__ == "__main__":
    receiver = audioReceiver("172.16.16.89", 9090) 