class connectedManager:
    def __init__(self):
        self.__connectedClients = {}
    
    def addClient(self, user):
        self.__connectedClients[user.getUserName()] = user