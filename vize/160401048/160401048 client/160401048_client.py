#Berkant Duman 160401048
import socket
import os


UDP_IP_ADDRESS = str(input("Lütfen sunucu ip adresini giriniz: "))
UDP_PORT_NO = 42
buffer_size = 9216

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = "Connected"
msg = msg.encode("utf-8")
try:
    clientSock.sendto(msg, (UDP_IP_ADDRESS, UDP_PORT_NO))
except:
    print("Bağlantı Hatası.")

while True:
    metod = str(input("Gerçekleştirmek istediğiniz komutu giriniz (LS, GET, PUT): "))

    if(metod.upper().startswith("GET")):
        msg = metod.encode("utf-8")
        try:
            clientSock.sendto(msg, (UDP_IP_ADDRESS, UDP_PORT_NO))
            file_data, adr = clientSock.recvfrom(buffer_size)
        except:
            print("Bağlantı hatası")

        if("Dosya bulunamadı.".encode("utf-8") != file_data):
            print("Dosya indiriliyor...")
            f = open(metod.split(" ")[1], 'wb')
            f.write(file_data)
            f.close()
            print("İndirme tamamlandı.")
        else:
            print(file_data.decode("utf-8"))

    elif(metod.upper().startswith("PUT")):
        msg = metod.encode("utf-8")
        try:
            clientSock.sendto(msg, (UDP_IP_ADDRESS, UDP_PORT_NO))
            filename = metod.split(" ")[1]
            print(filename)
        except:
            print("Bağlantı Hatası")

        if filename not in os.listdir():
            print("Dosya bulunamadı.")
        else:
            print("Dosya yükleniyor...")
            f = open(filename, "rb")
            fileData = f.read()
            try:
                clientSock.sendto(fileData, (UDP_IP_ADDRESS, UDP_PORT_NO))
                completed, adr = clientSock.recvfrom(buffer_size)
                print(completed.decode("utf-8"))
            except:
                print("Bağlantı Hatası")

    elif(metod.upper().startswith("LS")):
        msg = metod.encode("utf-8")
        try:
            clientSock.sendto(msg, (UDP_IP_ADDRESS, UDP_PORT_NO))
            data, adr = clientSock.recvfrom(buffer_size)
            liste = "Dosya listesi: \n" + data.decode("utf-8")
            print(liste)
        except:
            print("Bağlantı Hatası.")

    else:
        print("Yalnış komut girdiniz")
