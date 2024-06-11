from enum import Enum

class commandConstants(Enum):
    CONNECT_MSG = "!CONNECT"
    DISCONNECT_MSG = "!DISCONNECT_CLIENT"
    REQUEST_MSG = "!REQUEST"
    CLIENT_LIST_MSG = "!CLIENT_LIST"
    HEADER = 64
    FORMAT = 'utf-8'
    
