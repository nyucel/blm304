#Gizem Karagöl

import socket 
import datetime
from datetime import datetime 
import locale
locale.setlocale(locale.LC_ALL, '')


ip=input("\IP giriniz:")
port = 142

client=socket.socket()

try:
    client.connect((ip, port))
    a = s.recv(1024).decode()
    b = a.split(" ")
    s = float(b[0])
    suan = datetime.datetime.fromtimestamp(s)
    print(suan,"  ",b[1])
    
except socket.error as message:
    print("hata !" , message )
client.close()
komut='sudo date --set='
komut = komut + b[0]
os.system(komut)