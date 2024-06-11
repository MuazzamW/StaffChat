class connectedManager:
    def __init__(self):
        self.__connectedClients = {}
    
    def addClient(self, user):
        self.__connectedClients[user.getUserID()] = user
        
    def removeClient(self, userId):
        del self.__connectedClients[userId]

    def getClient(self, userId):
        return self.__connectedClients[userId]

    def getUserName(self, userId):
        return self.__connectedClients[userId].getUserName()
    
    def getThread(self, userId):
        return self.__connectedClients[userId].getThread()

    def getConnectedClients(self):
        return self.__connectedClients

    def checkIfConnected(self, userId):
        return userId in self.__connectedClients
    
    def returnClients(self):
        return self.__connectedClients