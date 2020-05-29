import socket
import os


ip_address = str(input("Lütfen sunucu ip adresini giriniz: "))
port_number = 42
buffer_size = 4096

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = "Connected"
msg = msg.encode("utf-8")
try:
    clientSock.sendto(msg, (ip_address, port_number))
except:
    print("Hata! Bağlantı Kurulamadı.")

while True:
    metod = str(input("Gerçekleştirmek istediğiniz komutu giriniz (LS, GET, PUT): "))

    if(metod.upper().startswith("GET")):
        msg = metod.encode("utf-8")
        try:
            clientSock.sendto(msg, (ip_address, port_number))
            file_data, adr = clientSock.recvfrom(buffer_size)
        except:
            print("Hata! Bağlantı Kurulamadı.")

        if("Dosya bulunamadı.".encode("utf-8") != file_data):
            print("Dosya indiriliyor...")
            f = open(metod.split(" ")[1], 'wb')
            f.write(file_data)
            f.close()
            print("İndirme başarıyla tamamlandı.")
        else:
            print(file_data.decode("utf-8"))

    elif(metod.upper().startswith("PUT")):
        msg = metod.encode("utf-8")
        try:
            clientSock.sendto(msg, (ip_address, port_number))
            filename = metod.split(" ")[1]
            print(filename)
        except:
            print("Hata! Bağlantı Kurulamadı.")

        if filename not in os.listdir():
            print("Dosya bulunamadı.")
        else:
            print("Dosya yükleniyor...")
            f = open(filename, "rb")
            fileData = f.read()
            try:
                clientSock.sendto(fileData, (ip_address, port_number))
                completed, adr = clientSock.recvfrom(buffer_size)
                print(completed.decode("utf-8"))
            except:
                print("Hata! Bağlantı Kurulamadı.")

    elif(metod.upper().startswith("LS")):
        msg = metod.encode("utf-8")
        try:
            clientSock.sendto(msg, (ip_address, port_number))
            data, adr = clientSock.recvfrom(buffer_size)
            liste = "Dosya listesi: \n" + data.decode("utf-8")
            print(liste)
        except:
            print("Hata! Bağlantı Kurulamadı.")

    else:
        print("Yalnış komut girdiniz")