class connectedManager:
    def __init__(self):
        self.__connectedClients = {}
    
    def addClient(self, user):
        self.__connectedClients[user.getUserID()] = user
        
    def removeClient(self, userId):
        del self.__connectedClients[userId]

    def getClientbyID(self, userId):
        return self.__connectedClients[userId]
    
    def getClientbyIP(self, ip):
        for client in self.__connectedClients:
            if self.__connectedClients[client].getAddress()[0] == ip:
                return self.__connectedClients[client]
        return None

    def getUserName(self, userId):
        return self.__connectedClients[userId].getUserName()
    
    def getThread(self, userId):
        return self.__connectedClients[userId].getThread()

    def returnClients(self):
        #print out client details for each client
        for client in self.__connectedClients:
            print(f"Client ID: {self.__connectedClients[client].getUserID()} \nUsername: {self.__connectedClients[client].getUserName()} \nIP: {self.__connectedClients[client].getAddress()[0]} \nPort: {self.__connectedClients[client].getAddress()[1]}") 

    def checkIfConnectedbyID(self, userId):
        return userId in self.__connectedClients
    
    def checkIfConnectedByIP(self, ip):
        for client in self.__connectedClients:
            if self.__connectedClients[client].getAddress()[0] == ip:
                return True
        return False

    def checkIfConnectedByUserName(self, userName):
        for client in self.__connectedClients:
            if self.__connectedClients[client] .getUserName() == userName:
                return True
    
    def getUserNamebyIP(self, ip):
        for client in self.__connectedClients:
            if self.__connectedClients[client].getAddress()[0] == ip:
                return self.__connectedClients[client].getUserName()
        return None
    
    def getClientbyUserName(self, userName):
        for client in self.__connectedClients:
            if self.__connectedClients[client].getUserName() == userName:
                return self.__connectedClients[client]
        return None

    def getConnectionbyIP(self, ip):
        for client in self.__connectedClients:
            if self.__connectedClients[client].getAddress()[0] == ip:
                return self.__connectedClients[client].getConnection()
        return None