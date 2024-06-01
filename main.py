import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname('www.google.com')
port = 90
s.connect((ip, port))