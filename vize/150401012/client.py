#Yiğit Yüre 150401012

import socket
import os
import sys


try:
    socket.gethostbyname(sys.argv[1])
except socket.error:
    print("Geçersiz IP adresi")
    sys.exit()
host = sys.argv[1]
port = int(sys.argv[2])

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("İstemci soketi başlatıldı")
except socket.error:
    print("Soket oluşturulamadı")
    sys.exit()

while True:
    komut = input("Bir komut giriniz: \n1. get [file_name]\n2. put [file_name]\n3. list\n ")
  
  IstemciKomutu = komut.encode('utf-8')
    try:
        s.sendto(IstemciKomutu, (host, port))
    except ConnectionResetError:
        print("Bağlantı port numaraları eşleşmiyor")
        sys.exit()
  
  KL = komut.split()

  if KL[0] == "get":
        try:
            ClientData, clientAddr = s.recvfrom(4096)
        except ConnectionResetError:
            print("Port numaraları eşleşmiyor")
            sys.exit()
        
        text = ClientData.decode('utf8')
        print(text)

        if len(text) < 30:
            Data, Recv = s.recvfrom(8192)
            dosya = open(KL[1], "wb")
            dosya.write(Data)
            dosya.close()
            print("Dosya alındı")

  elif KL[0] == "put":
        try:
            ClientData, clientAddr = s.recvfrom(4096)
        except ConnectionResetError:
            print("Port numaraları eşleşmiyor")
            sys.exit()
        
        text = ClientData.decode('utf8')
        print(text)
        
        if text == "Geçerli put komutu":
            if os.path.isfile(KL[1]):
                dosya = open(KL[1], "rb")
                Data = dosya.read()
                s.sendto(Data, clientAddr)
                print("Dosya yükleniyor")
                dosya.close()
            else:
                print("Dosya bulunamadı")
        else:
            print("Geçersiz komut")

  elif KL[0] == "list":
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print("Port numaraları eşleşmiyor")
            sys.exit()
        
        text = ClientData.decode('utf8')
        print(text)

        if text == "Geçerli list komutu":
            ClientDataL, clientAddrL = s.recvfrom(4096)
            text2 = ClientDataL.decode('utf8')
            print(text2)
        else:
            print("Geçersiz komut")