
#190401111 Atahan AKTAŞ

import socket
import os
import sys

host = input("IP Adresi Giriniz:")
port = int(input("Port Numarası Giriniz"))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((host, port))

cur_dir = s.recv(1024)
cur_dir = cur_dir.decode("utf-8")
while True:
   command = input("Lütfen Bir Komut Girin: \n ls=liste \n put:yükle \n get:çek \n")
    CommClient = command.encode("utf-8")
    try:
        s.sendto(CommClient, (host, port))
    except ConnectionResetError:
        print("HATA. Port Numarası Eşleşmiyor. Çıkılıyor. Bir Dahaki Sefere Aynı Port Numarasını Giriniz.")
        sys.exit()
    CL = command.split()

    if CL[0] == "get":
        print("Onay Kontrolü")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print("HATA. Port Numarası Eşleşmiyor. Çıkılıyor. Bir Dahaki Sefere Aynı Port Numarasını Giriniz.")
            sys.exit()
   elif CL[0] == "put":
        print("Onay Kontrolü")
        try:
            ClientData, clientAddr = s.recvfrom(4096)
        except ConnectionResetError:
            print("HATA. Port Numarası Eşleşmiyor. Çıkılıyor. Bir Dahaki Sefere Aynı Port Numarasını Giriniz.")
            sys.exit()

    elif CL[0] == "ls":
        print("Onay Kontrolü")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print("HATA. Port Numarası Eşleşmiyor. Çıkılıyor. Bir Dahaki Sefere Aynı Port Numarasını Giriniz.")
            sys.exit()

print("Program Sonlandırılıyor. ") 
quit()

