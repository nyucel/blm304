#Kadir Çolak 160401037
import socket
from datetime import datetime
import os


print('ip :', end =" ")
HOST = input()
PORT = 142

sent = 0
received = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    sent = datetime.utcnow().timestamp()
    s.sendall(b'hi')
    data = s.recv(32)
received = datetime.utcnow().timestamp()
dif = (received - sent)/2
s.close()

res = float(data.decode())
yenitimestamp = int(res + dif)
os.system("timedatectl set-ntp false")
os.system("date +%s -s @" + str(yenitimestamp))