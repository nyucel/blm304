
#190401111 - Atahan Aktaş

import socket
import os
import sys
from threading import Thread

host = "127.0.0.1"
port = int(input("PORT Numarası Giriniz"))

def create_socket():
    try:
        s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Soket Oluşturuldu.")
    except socket.error as msg:
        print("HATA:", str(msg))

def bind_socket():
    try:
        s.bind((host, port))
        print("Soket {} Numaralı Porta Bağlandı".format(port))
        s.listen(5)
        print("Port", port , "Dinleniyor.")
    except socket.error as msg:
        print("HATA:", str(msg))
        bind_socket()

def socket_accept():
    while True:
        c, addr = s.accept()
        print("Gelen Bağlantı: ", addr[0], ":", addr[1])
        try:
            Thread(target=send_data, args=(c, addr)).start()
        except:
            print("Hata")

def ServerList():
    print("Komut Gönderme Onaylandı.")
    msg = "Geçerli Liste Komutu. Devam Et."
    msgEn = msg.encode("utf-8")
    s.sendto(msgEn, clientAddr)
    print("Mesaj Gönderildi.")

    print("Sunucuda Liste Fonksiyonu")
    
    F = os.listdir(path="C:/Users/ataar/AppData/Local/Programs/Python/Python38")
    Lists = []
    
    for file in F:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode("utf-8")
    s.sendto(ListsEn, clientAddr)
    print("Sunucudan Gönderilen Liste")

def ServerGet(g):
    print("Komut Gönderme Onaylandı.")
    msg = "Geçerli Alma Komutu. Devam Et."
    msgEn = msg.encode("utf-8")
    s.sendto(msgEn, clientAddr)
    print("Mesaj Gönderildi.")

    if os.path.isfile(g):
        msg = "Dosya Var. Devam Et"
        msgEn = msg.encode("utf-8")
        s.sendto(msgEn, clientAddr)
        print("Dosyanın Varlığı Hakkında Gönderilen Mesaj.")

        c = 0
        size = os.stat(g)
        size2 = size.st_size  
        print("Bayt Cinsinden Dosya Boyutu:" + str(size2))
        Num = int(size2 / 4096)
        Num = Num + 1
        till = str(Num)
        till2 = till.encode("utf8")
        s.sendto(till2, clientAddr)

        check = int(Num)
        GetRun = open(g, "rb")
        while check != 0:
            Run = GetRun.read(4096)
            s.sendto(Run, clientAddr)
            c += 1
            check -= 1
            print("Paket Numarası:" + str(c))
            print("Veri Gönderme Devam Ediyor:")
        GetRun.close()

    else:
        msg = "HATA: Dosya, Sunucu Dizininde Mevcut Değil."
        msgEn = msg.encode("utf-8")
        s.sendto(msgEn, clientAddr)
        print("Mesaj Gönderildi.")

def ServerPut():
    print("Komut Gönderme Onaylandı.")
    msg = "Geçerli Verme Komutu. Devam Et."
    msgEn = msg.encode("utf-8")
    s.sendto(msgEn, clientAddr)
    print("Mesaj Gönderildi.")

    if t2[0] == "put":

        BigSAgain = open(t2[1], "wb")
        d = 0
        print("Dosya Varsa Paketlerin Alınması Şimdi Başlayacaktır.")
        try:
            Count, countaddress = s.recvfrom(4096)  
        except ConnectionResetError:
            print("HATA. Port Numarası Eşleşmiyor. Çıkılıyor. Bir Dahaki Sefere Aynı Port Numarasını Giriniz.")
            sys.exit()

        tillI = Count.decode("utf8")
        tillI = int(tillI)

        while tillI != 0:
            ServerData, serverAddr = s.recvfrom(4096)
            dataS = BigSAgain.write(ServerData)
            d += 1
            tillI = tillI - 1
            print("Alınan Paket Numarası:" + str(d))

        BigSAgain.close()
        print("Yeni Dosya Kapatıldı. Dizininizdeki İçeriği Kontrol Edin.")

def ServerElse():
    msg = "HATA: Sorun " + \
        t2[0] + "Sunucu Tarafından Anlaşılamamıştır."
    msgEn = msg.encode("utf-8")
    s.sendto(msgEn, clientAddr)
    print("Mesaj Gönderildi.")

while True:
    try:
        data, clientAddr = s.recvfrom(4096)
    except ConnectionResetError:
        print("HATA. Port Numarası Eşleşmiyor. Çıkılıyor. Bir Dahaki Sefere Aynı Port Numarasını Giriniz.")
        sys.exit()
    text = data.decode("utf8")
    t2 = text.split()

    if t2[0] == "Get":
        print("Get Fonksiyonuna Git")
        ServerGet(t2[1])
    elif t2[0] == "Put":
        print("Put Fonksiyonuna Git")
        ServerPut()
    elif(t2[0] == "ls"):
        print("ls Fonksiyonuna Git")
        ServerList()
    else:
        ServerElse()

print("Program Sona Erecek.")
quit()
