#Berkant Duman 160401048
import socket
import os


def server(IP):
    UDP_IP_ADDRESS = IP
    UDP_PORT = 42
    buffer_size = 9216
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((UDP_IP_ADDRESS, UDP_PORT))
    try:
        data, addr = serverSocket.recvfrom(buffer_size)
    except:
        print("Bağlantı hatası.")
    
    if addr:

        if(data.decode("utf-8").upper().startswith("GET")):

            filename = data.decode("utf-8").split(" ")[1]
            if filename not in os.listdir():
                serverSocket.sendto("Dosya bulunamadı.".encode("utf-8"), addr)
            else:
                f = open(filename, "rb")
                fileData = f.read()
                try:
                    serverSocket.sendto(fileData, addr)
                except:
                    print("Bağlantı hatası")

        elif(data.decode("utf-8").upper().startswith("PUT")):
            file_data, addr = serverSocket.recvfrom(buffer_size)
            f = open(data.decode("utf-8").split(" ")[1], 'wb')
            f.write(file_data)
            f.close()
            try:
                serverSocket.sendto(
                    "Yükleme tamamlandı.".encode("utf-8"), addr)
            except:
                print("Bağlantı hatası:")
        elif(data.decode("utf-8").upper().startswith("LS")):
            fileList = ""
            for i in os.listdir():
                if i != "160401048_server.py":
                    fileList += i + "\n"
            try:
                serverSocket.sendto(fileList.encode("utf-8"), addr)
            except:
                print("Bağlantı hatası ")

        else:
            print("Message: ", data.decode("utf-8"), "Adress: ", addr)

    else:
        print("Bağlantı hatası ")


print("Server Listining")
IP = str(input("Lütfen sunucu ip adresini giriniz: "))
while True:
    server(IP)
