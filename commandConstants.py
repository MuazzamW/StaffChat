from enum import Enum

class commandConstants(Enum):
    CONNECT_MSG = "!CONNECT"
    DISCONNECT_MSG = "!DISCONNECT_CLIENT"
    REQUEST_MSG = "!REQUEST"
    HEADER = 64
    FORMAT = 'utf-8'
    
