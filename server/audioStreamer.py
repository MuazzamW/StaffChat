import pyaudio
import socket

class audioStreamer:
    def __init__(self, serverIp, serverPort):
        self.__FORMAT = pyaudio.paInt16
        self.__CHANNELS = 2
        self.__RATE = 44100
        self.__CHUNK = 1024   
        self.p = pyaudio.PyAudio()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((serverIp, serverPort))
        self.server_socket.listen(1)
        print(f"Server listening on {serverIp}:{serverPort}...")
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Client connected: {self.client_address}")

        # Initialize audio stream
        self.sendAudio()
        
    def sendAudio(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.__FORMAT, channels=self.__CHANNELS, rate=self.__RATE, input=True, frames_per_buffer=self.__CHUNK)
        try:
            while True:
                # Read audio data
                data = stream.read(self.__CHUNK, exception_on_overflow=False)
                # Send audio data to the client
                self.__client_socket.sendall(data)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Cleanup
            stream.stop_stream()
            stream.close()
            audio.terminate()
            self.__client_socket.close()
            self.__server_socket.close()


if __name__ == "__main__":
    streamer = audioStreamer("172.16.16.89",9090)
