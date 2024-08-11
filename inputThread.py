import threading
import queue
import time

class inputThread:
    def __init__(self):
        super().__init__()
        self.__input_queue = queue.Queue()
        self.__prompt_lock = threading.Lock()


    # def run(self):
    #     while True:
    #         try:
    #             with self.__prompt_lock:
    #                 msg = input(self.__prompt)
    #             self.__input_queue.put(msg)
    #         except:
    #             print("An error occurred")
    #             break

    def getInput(prompt):
        with self.__prompt_lock:
            msg = input(prompt)
        return msg


    def stop(self):
        self.__running = False