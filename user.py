class User:
    def __init__(self, id, thread):
        self.__id = id
        self.__thread = thread
    
    def getUserID(self):
        return self.__id
    
    def getThread(self):
        return self.__thread