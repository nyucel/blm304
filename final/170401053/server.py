#Reber Ferhat Uluca - 170401053

import socket
import os
from datetime import datetime

utc_time = -3

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", 142))
    server.listen(5)
    print("Server is running...")
except:
    print("Socket error!")

epoch = datetime.fromtimestamp(0)

while True:
    clientsocket, address = server.accept()
    print("Connected :", address)
    utc = datetime.utcnow()
    utc_milliseconds = str(int((utc - epoch).total_seconds() * 1000 + utc_time * 3600000))
    print("sent: ", datetime.utcfromtimestamp(int(utc_milliseconds)//1000))
    clientsocket.send(utc_milliseconds.encode("utf-8"))