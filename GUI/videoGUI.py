import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk
import numpy as np

class VideoChatGUI(tk.Frame):
    def __init__(self,root):

        self.root = root
        self.root.title("Staff Chat")
        self.camera_off_image = Image.open("/Users/muazzamw/Desktop/Github_Projects/StaffChat/Assets/video_off.jpg")
        #resize image
        self.camera_off_image = self.camera_off_image.resize((200, 200))
        self.camera_off_image = ImageTk.PhotoImage(self.camera_off_image)

        # Create a label to display the video frames
        self.video_frame = Label(self.root)
        self.video_frame.pack(side=tk.LEFT, padx=10, pady=10)
        #change label colour
        self.video_frame.config(bg='black')
        #change label size
        

        # Create buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.start_button = Button(self.button_frame, text="Start Camera", command=self.start_camera)
        self.start_button.pack(pady=5)

        self.stop_button = Button(self.button_frame, text="Stop Camera", command=self.stop_camera)
        self.stop_button.pack(pady=5)

        self.end_call_button = Button(self.button_frame, text="End Call", command=self.root.destroy)
        self.end_call_button.pack(pady=5)

        #start with camera off image
        self.camera_off_image = ImageTk.PhotoImage(Image.open("/Users/muazzamw/Desktop/Github_Projects/StaffChat/Assets/video_off.jpg"))
        self.show_camera_off_image()

        # Flags for button states
        self.muted = False
        self.video_on = True

    def setVidStreamer(self,videoStreamer):
        self.__videoStreamer = videoStreamer

    def start_camera(self):
        self.__videoStreamer.cameraOn()
    
    def stop_camera(self):
        self.__videoStreamer.cameraOff()

    def show_camera_off_image(self):
        self.video_frame.config(image=self.camera_off_image)

    def getCameraOffImage(self):
        return self.camera_off_image

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoChatGUI(root)
    root.mainloop()