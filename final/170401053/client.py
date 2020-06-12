#Reber Ferhat Uluca - 170401053

import socket
import time
import os
from datetime import datetime

host = input("Enter the host ip address: ")
port = 142

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
except socket.error:
    print("Socket error! Please try again")

os.system("sudo timedatectl set-ntp false")

delay = time.time()
millisecond = int(client.recv(64).decode("utf-8"))
delay2 = time.time()

utc = millisecond/1000 + (delay2 - delay)
utc = datetime.fromtimestamp(utc).strftime('%Y-%m-%d %H:%M:%S.%f')
os.system("sudo timedatectl set-time '{}'".format(utc))
print("time changed:", utc)