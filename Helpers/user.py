class User:
    def __init__(self, id, thread, conn, addr, userName):
        self.__id = id
        self.__thread = thread
        self.__conn = conn
        self.__userName = userName
        self.__addr = addr
    
    def setUserName(self, userName):
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
    
    def getAddress(self):
        return self.__addr
    