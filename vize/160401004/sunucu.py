#Zeliha Döner 160401004
import socket
from ftplib import FTP  
import os
import select
import time
buf=1024


def dosya_listele():
    msg = "Liste getir komutu"
    msgEn = msg.encode('utf-8')
    s_s.sendto(msgEn, adres)
    print("Sunucuda listeleniyor..")

    F=os.listdir()
    Lists = []
    for file in F:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode('utf-8')
    s_s.sendto(ListsEn, adres)

def getfunc():
    file_name,adres=s_s.recvfrom(1024)
    if os.path.exists(file_name)==True:
        with open(file_name,"rb") as f:
            data=f.read(buf)
            while data!='':
                s_s.sendto(data,adres)
                data=f.read(buf)
                print("Dosya gönderildi")
                break

def putfunc():
    while True:
        data, addr = s_s.recvfrom(1024)
        data=data.decode('utf-8')
        if data:
            print ("Dosya adı:", data)
            file_name = data.strip()

        f = open(file_name, 'wb')

        while True:
            ready = select.select([s_s], [], [], 3)
            if ready[0]:
                data, addr = s_s.recvfrom(1024)
                f.write(data)
            else:
                print (file_name, "Bitti!" )
                f.close()
                break

s_ip="127.0.0.1"
s_port=42

s_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_s.bind((s_ip,s_port))


while True:
    mesaj , adres = s_s.recvfrom(4096)
    text = mesaj.decode('utf8')
    t2 = text.split()
    if t2[0] == "listele":
        dosya_listele()
    elif t2[0] == "get":
        getfunc()
    elif t2[0] == "put":
        putfunc()
    elif t2[0] == "exit":
        print("Program sonlandırıldı")
        break

s_s.close()