import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk
import cv2
import threading
import socket
import pickle
import struct
import numpy as np

class VideoChatGUI:
    def __init__(self, initiator = False, serverIp = None, serverPort = None):

        self.__port = 8080
        self.__ip = socket.gethostbyname(socket.gethostname())
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection = None
        self.__connectionAddr = None
        self.__initiator = initiator


        # self.root = root
        # self.root.title("Video Chat Application")

        # Initialize the video capture
        self.cap = cv2.VideoCapture(0)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Create a label to display the video frames
        # self.video_label = Label(self.root)
        # self.video_label.pack()

        # Create buttons
        # self.mute_button = Button(self.root, text="Mute Voice", command=self.toggle_mute)
        # self.mute_button.pack(side=tk.LEFT, padx=10, pady=10)

        # self.video_button = Button(self.root, text="Turn Off Video", command=self.toggle_video)
        # self.video_button.pack(side=tk.LEFT, padx=10, pady=10)

        # self.end_call_button = Button(self.root, text="End Call", command=self.end_call)
        # self.end_call_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Flags for button states
        self.muted = False
        self.video_on = True

        if initiator:
            self.listen()
        else:
            self.connect(serverIp, serverPort) 
        # Start video loop
        #self.update_video()
        #self.listen()
    
    def listen(self):
        self.__server.bind((self.__ip, self.__port))
        self.__server.listen()
        print(f"[LISTENING] video server is listening on {self.__server.getsockname()}")
        while True:
            self.__connection, addr = self.__server.accept()
            self.__connectionAddr = addr
            print(addr)
            print(f"[NEW CONNECTION] {addr} connected.")
            #start two threads to send video frames and receive video frames
            send_thread = threading.Thread(target=self.send_video)
            send_thread.daemon = True

            receive_thread = threading.Thread(target=self.receive_video)
            receive_thread.daemon = True

            #send_thread.start()
            receive_thread.start()
    
    def connect(self, ip,port):
        self.__server.connect((ip, port))

        send_thread = threading.Thread(target=self.send_video)
        send_thread.daemon = True

        receive_thread = threading.Thread(target=self.receive_video)
        receive_thread.daemon = True

        # send_thread.start()
        receive_thread.start()

            

    def send_video(self):
        #Check if the video should be displayed
        # while self.video_on:
        #     ret, frame = self.cap.read()
        #     if ret:
        #         frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         frame_data = pickle.dumps(frame)
        #         if not self.__initiator:
        #             self.__server.sendall(struct.pack("Q", len(frame_data)))
        #             self.__server.sendall(frame_data)
        #         else:
        #             self.__connection.sendall(struct.pack("Q", len(frame_data)))
        #             self.__connection.sendall(frame_data)
        #             print("sent")

        while True:
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, (640, 480))
            encoded_frame = cv2.imencode(".jpg", frame)[1].tobytes()
            if not self.__initiator:
                print("sending")
                self.__server.sendall(message)
                self.__server.sendall(message)
            else:
                self.__connection.sendall(message)
                self.__connection.sendall(message)

            
            # encoded_frame = cv2.imencode(".jpg", frame)[1]
            # data_array = np.array(encoded_frame)
            # byte_encode = data_array.tobytes()
            # if not self.__initiator:
            #     self.__server.send(byte_encode)
            # else:
            #     self.__connection.send(byte_encode)


        # Schedule the next frame update
        #self.root.after(10, self.send_video)
    
    def receive_video(self):
        print("receiving")
        data = b""
        payload_size = struct.calcsize("Q")
        while True:
            while len(data) < payload_size:
                packet = self.__server.recv(4 * 1024)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += self.__server.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            #display frame onto the label
            # img = Image.fromarray(frame)
            # imgtk = ImageTk.PhotoImage(image=img)
            # self.video_label.imgtk = imgtk
            # self.video_label.configure(image=imgtk)

        # data = b""
        # while True:
        #     if not self.__initiator:
        #         packet = self.__server.recv(4 * 1024)
        #     else:
        #         packet = self.__connection.recv(4 * 1024)
        #     if not packet:
        #         break
        #     data += packet
        #     print(data)
            # data_array = np.frombuffer(data, dtype=np.uint8)
            # frame = cv2.imdecode(data_array, cv2.IMREAD_COLOR)
            # cv2.imshow("frame", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break


    # def toggle_mute(self):
    #     self.muted = not self.muted
    #     if self.muted:
    #         self.mute_button.config(text="Unmute Voice")
    #         # Add logic to mute voice
    #     else:
    #         self.mute_button.config(text="Mute Voice")
    #         # Add logic to unmute voice

    # def toggle_video(self):
    #     self.video_on = not self.video_on
    #     if self.video_on:
    #         self.video_button.config(text="Turn Off Video")
    #     else:
    #         self.video_button.config(text="Turn On Video")
    #         self.video_label.configure(image=r"video_off.jpg")

    # def end_call(self):
    #     # Add logic to end the call
    #     self.cap.release()
    #     self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoChatGUI(initiator=False, serverIp="172.16.16.24", serverPort=8080)