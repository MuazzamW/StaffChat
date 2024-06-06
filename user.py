class User:
    def __init__(self, userName, thread):
        self.__username = userName
        self.__thread = thread
    
    def getUserName(self):
        return self.__username
    
    def getThread(self):
        return self.__thread