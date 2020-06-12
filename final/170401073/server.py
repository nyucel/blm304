#Mehmet Salih Çelik 170401073
import time
import datetime
import socket

HOST =""
PORT = 142

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

def utchesapla():
    x = datetime.datetime.now()
    y = str(x.astimezone().timetz())
    z = y.strip()[15:18]
    if z[1]=="0":
        z=z[0]+z[2]
    else:
        z=z[0]+z[1]+z[2]
    return z

while True:
    print("Sunucunun kendi UTC degeri :",utchesapla())
    UTC = int(utchesapla())
    if UTC<0:
        print("Ayarlanmasi istenen zaman : UTC"+str(UTC))
    else:
        print("Ayarlanmasi istenen zaman : UTC+"+str(UTC))
    if UTC>int(utchesapla()):
        print("Istemci calistirildiginda, sunucudan ",int(UTC)-int(utchesapla())," saat ileride olmali \n")
    elif UTC<int(utchesapla()):
        print("Istemci calistirildiginda, sunucudan ", int(utchesapla())-int(UTC) , " saat geride olmali \n")
    else:
        print("Istemci calistirildiginda, sunucu saati ile ayni olmali. \n")
    conn, addr = s.accept()
    x = (datetime.datetime.now().timestamp() * 1000) // 1
    y= str(x)+" UTC: "+str(UTC)
    data = y.encode("utf-8")
    conn.sendall(data)

s.close()
