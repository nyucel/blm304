# -*- coding: utf-8 -*-
"""
@author: Halil İbrahim Koç
"""



import socket
import time
import os
import sys

port=70
buffer=4096

if len(sys.argv) != 2:
    print("Host bilgisi girilmelidir.")
    sys.exit()

try:
    socket.gethostbyname(sys.argv[1])
except socket.error:
    print("Host bilgisi gereklidir. Kontrol edip tekrar deneyiniz.")
    sys.exit()

host = sys.argv[1]
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Bağlantı başlatılıyor")
    s.setblocking(0)
    s.settimeout(15)
except socket.error:
    print("Başarısız bağlantı")
    sys.exit()

while True:
    command = input(
        "Aşağıdaki komutlardan birini giriniz: \n1. get [dosya ismi]\n2. put [dosya ismi]\n3. list\n4. exit\n ")

    """o get [dosya ismi]
    o put [dosya ismi]
    o list
    o exit"""
    clientCommand = command.encode('utf-8')
    try:
        s.sendto(clientCommand, (host, port))
    except ConnectionResetError:
        print(
            "Port bilgisi yanlış.")
        sys.exit()
    clientArguments = command.split()

    if clientArguments[0] == "get":
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except:
            print("Program zaman aşımına uğradı.")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)


        try:
            ClientData2, clientAddr2 = s.recvfrom(buffer)

        except:
            print("Program zaman aşımına uğradı.")
            sys.exit()

        text2 = ClientData2.decode('utf8')
        print(text2)

        if len(text2) < 50:
            
            if clientArguments[0] == "get":
                ComingFile = open(clientArguments[1], "wb")
                d = 0
                try:
                    # number of paclets
                    CountC, countaddress = s.recvfrom(buffer)
                except:
                    print("Bağlantı zaman aşımına uğradı.")
                    sys.exit()

                packet1 = CountC.decode('utf8')
                packet12 = int(packet1)
                

                while packet12 != 0:
                    ClientBData, clientbAddr = s.recvfrom(4096)
                    
                    dataS = ComingFile.write(ClientBData)
                    d += 1
                    print("Paket Adedi:" + str(d))
                    packet12 = packet12 - 1

                ComingFile.close()
                print(
                    "Dosya indirildi.")

    elif clientArguments[0] == "put":
        try:
            ClientData, clientAddr = s.recvfrom(buffer)
        except:
            print("Bağlantı zaman aşımına uğradı.")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)

        if text == "Put fonksiyonu başlatıldı.":
            if os.path.isfile(clientArguments[1]):

                c = 0
                #Length = len(CL1[1])

                size = os.stat(clientArguments[1])
                sizeS = size.st_size  # number of packets
                #sizeS = sizeS[:-1]
                print("Dosya boyutu(bayt): " + str(sizeS))
                Num = int(sizeS / buffer)
                Num = Num + 1
                print("Gönderilen Paket Sayısı: " + str(Num))

                s.sendto(str(Num).encode('utf8'), clientAddr)
                
                packet_num = int(Num)
                SendingFile = open(clientArguments[1], "rb")

                while packet_num != 0:
                    Run = SendingFile.read(buffer)
                    s.sendto(Run, clientAddr)
                    c += 1
                    packet_num -= 1
                    print("Paket Sayısı:" + str(c))
                    

                SendingFile.close()

                print("İstemciden sunucuya put işlemi sona erdi.")
                # s.sendto(str(sizeS).encode('utf8'),clientAddr)
            else:
                print("İstemcinin bulunduğu dizinde dosya bulunamadı.")
        else:
            print("Geçersiz.")

    elif clientArguments[0] == "list":
        try:
            ClientData, clientAddr = s.recvfrom(buffer)
            ClientData2, clientAddr2 = s.recvfrom(buffer)
        except:
            print("Bağlantı zaman aşımına uğradı.")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)
        lists=ClientData2.decode('utf8')
        print("Server'daki dosyalar:")
        lists=lists.split(',')
        for i in lists:
            print(i)

    elif clientArguments[0] == "exit":
        print(
            "Client ve Server kapatılıyor.")
        quit()

print("Client kapatıldı.")
