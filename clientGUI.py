import tkinter as tk
from tkinter import scrolledtext
import threading
import socket
from commandConstants import commandConstants
from videoSender import videoSender

class clientGUI:

    def __init__(self, client, pingserver):
        self.pingserver = pingserver
        self.client = client
        self.root = tk.Tk()
        self.root.title("Client Chat")

        # Output area for the main server messages
        self.server_output = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20)
        self.server_output.grid(row=0, column=0, padx=10, pady=10)

        # Text box to send messages to the main server
        self.message_input = tk.Entry(self.root, width=50)
        self.message_input.grid(row=1, column=0, padx=10, pady=10)
        self.message_input.bind("<Return>", self.send_message)

        # Output area for the ping server messages
        #make it uneditable

        self.ping_output = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=10)
        self.ping_output.grid(row=2, column=0, padx=10, pady=10)
        self.ping_output.config(state=tk.DISABLED)

        # Start receiving messages from the server
        self.receive_thread = threading.Thread(target=self.receive_message)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # Start receiving ping responses
        self.ping_thread = threading.Thread(target=self.receive_ping)
        self.ping_thread.daemon = True
        self.ping_thread.start()

    def update_ping_output(self, message):
        self.ping_output.config(state=tk.NORMAL)  # Temporarily make it editable
        self.ping_output.insert(tk.END, message + '\n')  # Insert the new message
        self.ping_output.config(state=tk.DISABLED)  # Make it non-editable again
        self.ping_output.yview(tk.END)

    def send_message(self, event=None):
        message = self.message_input.get()
        self.client.write(message)
        self.message_input.delete(0, tk.END)
        self.server_output.insert(tk.END, f"You: {message}\n")
        self.server_output.yview(tk.END)

    def receive_message(self):
        while True:
            try:
                msg_length = self.client.getServer().recv(self.client.HEADER).decode(self.client.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.client.getServer().recv(msg_length).decode(self.client.FORMAT)
                    self.server_output.insert(tk.END, f"Server: {msg}\n")
                    self.server_output.yview(tk.END)
                    match msg:
                        case commandConstants.ACCEPTED.value:
                            print("Request accepted, starting stream...")
                            #start video and audio stream
                            videoSender(self.client.getAddr(),8080)
                        case commandConstants.DENIED.value:
                            print("Request denied")
                        case _:
                            pass
            except Exception as e:
                self.server_output.insert(tk.END, f"Error: {e}\n")
                self.server_output.yview(tk.END)
                break
    
    def receive_ping(self):
        while True:
            try:
                msg_length = self.pingserver.recv(self.client.HEADER).decode(self.client.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = self.pingserver.recv(msg_length).decode(self.client.FORMAT)
                    self.update_ping_output(msg)
                    if msg == commandConstants.PING_MSG.value:
                        self.client.write(commandConstants.PONG_MSG.value)
            except Exception as e:
                self.ping_output.insert(tk.END, f"Ping Error: {e}\n")
                self.ping_output.yview(tk.END)
                break

    def run(self):
        self.root.mainloop()