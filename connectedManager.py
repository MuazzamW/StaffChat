class connectedManager:
    def __init__(self):
        self.__connectedClients = {}
    
    def addClient(self, userId, user):
        self.__connectedClients[userId] = user
        
    def removeClient(self, userId):
        del self.__connectedClients[userId]
    
    def getThread(self, userId):
        return self.__connectedClients[userId].getThread()

    def getConnectedClients(self):
        return self.__connectedClients

    def checkIfConnected(self, userId):
        return userId in self.__connectedClients