class User:
    def __init__(self, id, thread, conn, userName):
        self.__id = id
        self.__thread = thread
        self.__conn = conn
        self.__userName = userName
    
    def setThread(self, thread):
        self.__thread = thread
    
    def getUserName(self):
        return self.__userName

    def getUserID(self):
        return self.__id
    
    def getThread(self):
        return self.__thread
    
    def getConnection(self):
        return self.__conn