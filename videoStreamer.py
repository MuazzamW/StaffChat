# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ip = socket.gethostbyname('www.google.com')
# port = 90
# s.connect((ip, port))

import cv2 as cv

class videoStreamer:
    def __init__(self):
        self.__camera = cv.VideoCapture(0)


    def getFrame(self):
        ret, frame = self.__camera.read()
        return frame
    
    def release(self):
        self.__camera.release()
        cv.destroyAllWindows()
    
    def encodeFrame(self, frame):
        return cv.imencode('.jpg', frame)[1].tobytes()
    
    def streamVideo(self):
        while True:
            frame = self.getFrame()
            cv.imshow('frame',frame)
            encoded = self.encodeFrame(frame)
            print(encoded)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        self.release()
        
        
if __name__ == "__main__":
    streamer = videoStreamer()
    streamer.streamVideo()
