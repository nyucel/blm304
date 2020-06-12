import socket
import os
import time
import select

hostname=socket.gethostname()
serverip=socket.gethostbyname(hostname)

port=42
bufferSize=1024
timeout=3

def filelist():
    filelist = os.listdir()
    fb=""
    for f in filelist:
        fb=fb+f+","
    fb=fb.encode()
    return fb

s=socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
s.bind((serverip,port))

print("Sunucu baslatildi")
print(serverip)
print("Client bekleniyor...")

fromclient=s.recvfrom(bufferSize)

message=fromclient[0]
clientip=fromclient[1]
print("Baglandi:")
print(clientip)

s.sendto(filelist(),clientip)

def get():
    fromclient = s.recvfrom(bufferSize)
    istek=fromclient[0].decode()

    s.sendto(istek.encode(),clientip)

    f = open(istek, "rb")
    data=f.read(bufferSize)
    while(data):
        if(s.sendto(data,clientip)):
            data = f.read(bufferSize)
            time.sleep(0.02)
    f.close()
    try:
        s.recvfrom(bufferSize)
    except socket.error:
        print("Baglanti koptu.Dosya gonderilemedi.")
    return
def put():
    fromclient = s.recvfrom(bufferSize)
    dosyaadi=fromclient[0].decode()
    f=open(dosyaadi,'wb')
    
    while True:
        ready = select.select([s], [], [], timeout)
        if ready[0]:
            data,addr=s.recvfrom(1024)
            f.write(data)
        else:
            f.close()
            s.sendto("1".encode(),clientip)
            break
    try:
        s.recvfrom(bufferSize)
    except socket.error:
        print("Baglanti koptu.Dosya aktarimi tamamlanamadi.")
        return
    else:
        print(dosyaadi,"sunucuya yuklendi.")
        return

while True:
    komut=s.recvfrom(bufferSize)[0].decode()

    if komut=="GET":
        get()
    if komut=="PUT":
        put()
    if komut=="LIST":
        print(filelist())
        s.sendto(filelist(),clientip)