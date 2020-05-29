import socket
import select
import time
import os

hostname = socket.gethostname()
localIP = socket.gethostbyname(hostname)
send=str.encode(localIP)
port=42
bufferSize=1024
timeout=3

serverip=input("Sunucu IP'si gir: ")
serveripport=(serverip,port)

s=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)

s.connect(serveripport)

def clientd():
    return os.listdir()

try:
    s.sendto(send,serveripport) 
except:
    print("Sunucu bulunamadi.")
    exit()

try:
    msgFromServer=s.recvfrom(bufferSize)
except:
    print("Sunucu bulunamadi.")
    exit()


def get(dosya):
    if dosya not in filelist:
        print("Dosya sunucuda bulunamadi.")
        return
    s.sendto("GET".encode(),serveripport)
    s.sendto(dosya.encode(),serveripport)
    while True:
        data,addr=s.recvfrom(bufferSize)
        if data:
            print(data.decode()," indiriliyor...")
            file_name = data.strip()
        f=open(file_name, 'wb')
        while True:
            ready = select.select([s], [], [], timeout)
            if ready[0]:
                data,addr=s.recvfrom(1024)
                f.write(data)
            else:
                print("Indirme tamamlandi.")
                f.close()
                s.sendto("1".encode(),serveripport)
                break
        break
    return          

def put(dosya):
    s.sendto("PUT".encode(),serveripport)
    s.sendto(dosya.encode(),serveripport)

    f=open(dosya,"rb")
    data=f.read(bufferSize)
    while(data):
        if(s.sendto(data,serveripport)):
            data = f.read(bufferSize)
            time.sleep(0.02)
    f.close()
    try:
        s.recvfrom(bufferSize)
    except socket.error:
        print("Baglanti koptu.Dosya gonderilemedi.")
    else:
        print(dosya,"sunucuya yuklendi.")
        s.sendto("1".encode(),serveripport)
    return

msg=msgFromServer[0].decode()
filelist=msg.split(",")
filelist.pop()
print("Dosyalar:")
for f in filelist:
    print(f)

komutlar=("GET","PUT","EXIT","LIST")

def menu():
    secim=""
    while True:
        secim=input("Islem gir (GET dosya_adi | PUT dosya_adi | LIST | EXIT)\n")
        if secim.split()[0] in komutlar:
            break
    
    secimd=secim.split(" ")

    if secimd[0]=="GET":
        get(secimd[1])
    if secimd[0]=="PUT":
        if secimd[1] not in clientd():
            print("Dosya bulunamadi.")
        else:
            put(secimd[1])
    if secimd[0]=="LIST":
        s.sendto(secimd[0].encode(),serveripport)
        msgFromServer=s.recvfrom(bufferSize)
        msg=msgFromServer[0].decode()
        filelist=msg.split(",")
        filelist.pop()
        print("Dosyalar:")
        for f in filelist:
            print(f)
    if secimd[0]=="EXIT":
        exit()

while True:
    menu()