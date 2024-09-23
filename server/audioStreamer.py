import pyaudio

class audioStreamer:
    def __init__(self):
        self.__FORMAT = pyaudio.paInt16
        self.__CHANNELS = 1
        self.__RATE = 44100
        self.__CHUNK = 1024   
        self.p = pyaudio.PyAudio()
    
    def getStream(self):
        return self.p.open(format=self.__FORMAT,
                channels=self.__CHANNELS,
                rate=self.__RATE,
                input=True,
                frames_per_buffer=self.__CHUNK)