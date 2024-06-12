class connectedManager:
    def __init__(self):
        self.__connectedClients = {}
    
    def addClient(self, user):
        self.__connectedClients[user.getUserID()] = user
        
    def removeClient(self, userId):
        del self.__connectedClients[userId]

    def getClientbyID(self, userId):
        return self.__connectedClients[userId]

    def getUserName(self, userId):
        return self.__connectedClients[userId].getUserName()
    
    def getThread(self, userId):
        return self.__connectedClients[userId].getThread()

    def returnClients(self):
        return self.__connectedClients

    def checkIfConnectedbyID(self, userId):
        return userId in self.__connectedClients
    
    def checkIfConnectedByIP(self, ip):
        for client in self.__connectedClients:
            if self.__connectedClients[client].getAddress()[0] == ip:
                return True
        return False