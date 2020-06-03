#Yiğit Yüre 150401012

import socket
import os
import sys


def ServerList():
    msg = "Geçerli list komutu"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Mesaj sunucuya iletildi")

    F = os.listdir(path="C:\Users\yigit\OneDrive\Masaüstü\150401012")
    Lists = []
    for file in F:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode('utf-8')
    s.sendto(ListsEn, clientAddr)
    print("Liste sunucudan gönderildi")

def ServerGet(g):
    msg = "Geçerli get komutu"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Mesaj istemciye gönderildi")

    if os.path.isfile(g):
        msg = "Dosya bulunuyor"
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)

        dosyaS = open(g, "wb")
        s.sendto(dosyaS, clientAddr)
        dosyaS.close()
    
    else:
        msg = "Dosya bulunamadı"
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)

def ServerPut():
    msg = "Geçerli put komutu"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Mesaj sunucuya iletildi")

    if t[0] == "put":
        BigSAgain = open(t2[1], "wb")

        ServerData, serverAddr = s.recvfrom(4096)
        dataS = BigSAgain.write(ServerData)
        BigSAgain.close()
        print("Yeni dosya kapatıldı")


host = ""
port = 42

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Sunucu soketi balşatıldı")
    s.bind((host, port))
    print("Bağlantı sağlandı, istemci bekleniyor")
except socket.error:
    print("Soket oluşturulamadı")
    sys.exit()

while True:
    try:
        data, clientAddr = s.recvfrom(4096)
    except ConnectionResetError:
        print("Port numaraları eşleşmiyor")
        sys.exit()

    text = data.decode('utf8')
    t = text.split()

    if t[0] == "get":
        ServerGet(t[1])
    elif t[0] == "put":
        ServerPut()
    elif t[0] == "list":
        ServerList()

quit()