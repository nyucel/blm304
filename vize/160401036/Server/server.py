#Hakan Reşit YALÇIN    -    160401036

import os
import socket
import sys
from threading import Thread

HOST = "127.0.0.1"
PORT=int(input("PORT NUMARASINI GİRİNİZ :    "))


def SOCKET_OLUSTUR():
    try:
        global HOST
        global PORT
        global sd
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Socket oluşturulamadı!", str(e))


def SOCKET_BAGLAN():
    try:
        global HOST
        global PORT
        global sd

        sd.bind((HOST, PORT))
        sd.listen(5)
        print(PORT, "Numaralı PORT bağlantısı sağlandı,dinlemede..")
    except socket.error as e:
        print("Socket oluşturulamadı!", str(e), "\nTekrar deneniyor...")
        SOCKET_BAGLAN()


def SOCKET_KONTROL():
    while True:
        baglanti, address = sd.accept()
        print("BAĞLANTI KURULUMU BAŞARILI. BAĞLANILAN IP: ", address[0], ":", address[1])
        try:
            Thread(target=VERI_TRANSFER, args=(baglanti, address)).start()
        except:
            print("ERROR")


def LISTELEME_KOMUTU(baglanti):
    veriler = os.listdir()
    veriler = [i+str("\n") for i in veriler]
    
    size = str(len(veriler))
    baglanti.send(str.encode(size))
  
    for d in veriler:
        d = str(d)
        
        baglanti.send(str.encode(d))
        l = baglanti.recv(10)
        


def GET_KOMUTU(baglanti, dosya_ismi):
    adet = baglanti.recv(20)
    baglanti.send(str.encode("SUCCESS"))
    if adet.decode("utf-8") == "$all_$":
        path = os.getcwd()
        dosyalar = [f for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))]
        ssize = len(dosyalar)
        baglanti.send(str.encode(str(ssize)))
        n = baglanti.recv(10)
        for a_file in dosyalar:
            baglanti.send(str.encode(str(a_file)))
            n = baglanti.recv(10)
            with open(str(a_file), "rb") as f:
                l = f.read(1024)
                while (l):
                    baglanti.send(l)
                    n = baglanti.recv(10)
                    
                    l = f.read(1024)
                baglanti.send(str.encode("$end$"))
    else:
        cur_path = os.getcwd()
        if os.path.exists(dosya_ismi):
            baglanti.send(str.encode("$present$"))
            istry = baglanti.recv(20)
            if istry.decode("utf-8") == "SUCCESS":
                with open(dosya_ismi, "rb") as f:
                    f = open(dosya_ismi, 'rb')
                    l = f.read(1024)
                    while (l):
                        baglanti.send(l)
                        n = baglanti.recv(10)
                        print("SUCCESS", repr(n))
                        l = f.read(1024)
                    
                    baglanti.send(str.encode("$end$"))
                    f.close()
        else:
            baglanti.send(str.encode("İSTENİLEN DOSYA BULUNAMADI!"))


def PUT_KOMUTU(baglanti, dosya_ismi):
    adet = baglanti.recv(20)
    baglanti.send(str.encode("SUCCESS"))
    if adet.decode("utf-8") == "$all$":
        ssize = baglanti.recv(20)
        baglanti.send(str.encode("SUCCESS"))
        for i in range(int(ssize)):
            fff_name = baglanti.recv(100)
            fff_name = fff_name.decode("utf-8")
            baglanti.send(str.encode("SUCCESS"))
            with open(fff_name, 'wb') as f:
                veri = baglanti.recv(1024)
                while True:
                    f.write(veri)
                    baglanti.send(str.encode("SUCCESS"))
                    veri = baglanti.recv(1024)
                    if veri.decode("utf-8") == "$end$":
                        print(veri.decode("utf-8"))
                        break
    else:
        with open(dosya_ismi, 'wb') as f:
            veri = baglanti.recv(1024)
            while True:
                f.write(veri)
                baglanti.send(str.encode("SUCCESS"))
                veri = baglanti.recv(1024)
                if veri.decode("utf-8") == "":
                    print(veri.decode("utf-8"))
                    break
                


def VERI_TRANSFER(baglanti, a):
    send_dir = os.getcwd()
    baglanti.send(str.encode(str(send_dir)))
    while True:
        veri = baglanti.recv(1024)
        veri = veri.decode("utf-8")
        r_cmd = veri.split(" ")
        cmd = r_cmd[0]
        try:
            dosya_ismi = r_cmd[1]
        except:
            pass
        if(cmd == "ls"):
            LISTELEME_KOMUTU(baglanti)
        elif(cmd == "get"):
            GET_KOMUTU(baglanti, dosya_ismi)
        elif(cmd == "put"):
            PUT_KOMUTU(baglanti, dosya_ismi)
    
        else:
            d = "GİRİLEN KOMUT GEÇERSİZ.YALNIZCA ls,put VE get KULLANINIZ!"


def main():
    SOCKET_OLUSTUR()
    SOCKET_BAGLAN()
    SOCKET_KONTROL()
    time.sleep(1)

main()
