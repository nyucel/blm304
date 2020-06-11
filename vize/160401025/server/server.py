# -*- coding: utf-8 -*-
"""
@author: Halil İbrahim Koç
"""



import socket
import time
import os
import sys



def List():
    s.sendto(("Server listeleme fonksiyonu başlatıldı.").encode('utf-8'), clientAddr)

    path=os.getcwd()
    File = os.listdir(path)

    Lists = []
    for file in File:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode('utf-8')
    s.sendto(ListsEn, clientAddr)


def Exit():

    print(
        "Sistem başarılı bir şekilde sonlanıyor.")
    s.close()  # closing socket
    sys.exit()


def Get(file):
    s.sendto(("Get fonksiyonu başlatıldı.").encode('utf-8'), clientAddr)
  

    if os.path.isfile(file):
        s.sendto(("Dosya Server'da bulunmakta. Devam ediliyor.").encode('utf-8'), clientAddr)

        c = 0
        sizeFiles = os.stat(file)
        sizeFile = sizeFiles.st_size  # number of packets
        print("Dosya Boyutu bytes:" + str(sizeFile))
        packet_number = int(sizeFile / buffer)
        packet_number = packet_number + 1

        s.sendto(str(packet_number).encode('utf8'), clientAddr)
        
        check = int(packet_number)
        ComingFile = open(file, "rb")
        while check != 0:
            RunS = ComingFile.read(buffer)
            s.sendto(RunS, clientAddr)
            c += 1
            check -= 1
            print("Paket Sayısı:" + str(c))
        ComingFile.close()
        print("Server get fonksiyonu sonlandırıldı.")

    else:
        s.sendto(("Dosya Server'da bulunamadı.").encode('utf-8'), clientAddr)


def Put():
    s.sendto(("Put fonksiyonu başlatıldı.").encode('utf-8'), clientAddr)

    if arguments[0] == "put":

        savedFile = open(arguments[1], "wb")
        d = 0

        try:
            Count, countaddress = s.recvfrom(buffer)  # number of packet
        except:
            print("Bağlantı zaman aşımına uğradı.")
            sys.exit()

        data = Count.decode('utf8')
        packet_num = int(data)


        while packet_num != 0:
            ServerData, serverAddr = s.recvfrom(buffer)

            dataS = savedFile.write(ServerData)
 
            d += 1
            packet_num = packet_num - 1
            print("Alınan Paket Adedi:" + str(d))
        
        # if os.stat(savedFile).st_size==os.stat(data).st_size:
        #     print("Gönderilen ")
        savedFile.close()
        print("Dosya kaydedildi.")
        # SizeData, SizeAddr = s.recvfrom(buffer)
        # print("Kayıt edilen datanın boyutu"int(SizeData.decode('utf8')))
def Else():
    s.sendto(("Girilen argüman geçersizdir.-->" + arguments[0]).encode('utf-8'), clientAddr)
    

host = socket.gethostbyname(socket.gethostname())
port = 70
buffer=4096
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Sunucu başlatıldı...")
    s.bind((host, port))
    print("Bağlantı başarılı. İstek bekleniyor...")

except socket.error:
    print("Bağlantı başlatılırken bir sorun oluştu!")
    sys.exit()


while True:
    try:
        data, clientAddr = s.recvfrom(buffer)
    except ConnectionResetError:
        print(
            "Port bilgisi yanlış!")
        sys.exit()
    text = data.decode('utf8')
    print(clientAddr)
    arguments = text.split()
   
    if arguments[0] == "get":
        print("Dosya indirilecek.")
        Get(arguments[1])
    elif arguments[0] == "put":
        print("Dosya kaydedilecek.")
        Put()
    elif arguments[0] == "list":
        print("Sunucudaki dosyalar listeleniyor...")
        List()
    elif arguments[0] == "exit":
        print("Çıkış")
        Exit()
    else:
        Else()

quit()