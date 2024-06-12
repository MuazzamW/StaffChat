from enum import Enum

class commandConstants(Enum):
    DISCONNECT_MSG = "!DISCONNECT_CLIENT"
    SEND_IP = "!SEND_IP"
    USERNAME = "!USERNAME"
    REQUEST_MSG = "!REQUEST"
    CLIENT_LIST_MSG = "!CLIENT_LIST"
    HEADER = 64
    FORMAT = 'utf-8'
    
