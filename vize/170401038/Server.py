#İsmail ALTAY 170401038

import socket
import os


def server(IP):
    ip_address = IP
    port = 42
    buffer_size = 4096
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((ip_address, port))
    try:
        data, address = serverSocket.recvfrom(buffer_size)
    except:
        print("Hata! Bağlantı Kurulamadı.")

    if address:

        if (data.decode("utf-8").upper().startswith("GET")):

            filename = data.decode("utf-8").split(" ")[1]
            if filename not in os.listdir():
                serverSocket.sendto("Dosya bulunamadı.".encode("utf-8"), address)
            else:
                f = open(filename, "rb")
                fileData = f.read()
                try:
                    serverSocket.sendto(fileData, address)
                except:
                    print("Hata! Bağlantı Kurulamadı.")

        elif (data.decode("utf-8").upper().startswith("PUT")):
            file_data, address = serverSocket.recvfrom(buffer_size)
            f = open(data.decode("utf-8").split(" ")[1], 'wb')
            f.write(file_data)
            f.close()
            try:
                serverSocket.sendto(
                    "Yükleme başarıyla tamamlandı.".encode("utf-8"), address)
            except:
                print("Hata! Bağlantı Kurulamadı.")
        elif (data.decode("utf-8").upper().startswith("LS")):
            fileList = ""
            for i in os.listdir():
                if i != "170401038_server.py":
                    fileList += i + "\n"
            try:
                serverSocket.sendto(fileList.encode("utf-8"), address)
            except:
                print("Hata! Bağlantı Kurulamadı.")

        else:
            print("Message: ", data.decode("utf-8"), "Adress: ", address)

    else:
        print("Hata! Bağlantı Kurulamadı.")


print("Server Dinleniyor..")
IP = str(input("Lütfen sunucu ip adresini giriniz: "))
while True:
    server(IP)