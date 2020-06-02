import socket
import os
import time
import sys
#MELİSA BAYRAMLI 140401052



print ("\nFTP sunucusuna hoş geldiniz. \n Başlamak için bir istemci bağlayın.")
localIP = "127.0.0.1"
localPort = 42
BUFFER_SIZE=4096
mklasor=os.listdir()
serverDirectory="Server Directory"

if serverDirectory not in mklasor:
    os.mkdir(serverDirectory)
    print("Server directory oluşturuldu... ")
else:
    print("Directory zaten var... ")
os.chdir(serverDirectory)
try:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((localIP, localPort))
except:
    print("HATA sunucu olusturma basarisiz..")
    sys.exit()

while True:

    a=0
    while a<1:
        print("Server dinlemede....")
        bytesAddressPair=udp_socket.recvfrom(BUFFER_SIZE)
        mes=bytesAddressPair[0].decode()
        addr=bytesAddressPair[1]
        komut =mes[:3]
        file_title=mes[:4]

        if komut=="PUT":
            data=udp_socket.recvfrom(BUFFER_SIZE)[0]
            file=open(data.strip(),"wb")
            data=udp_socket.recvfrom(BUFFER_SIZE)
            try:
                while data:
                    data=udp_socket.recvfrom(BUFFER_SIZE)[0]
                    file.write(data)
                    udp_socket.settimeout(3)
            except socket.timeout:
                file.close()
            udp_socket.sendto(b"True",addr)
        elif komut=="GET":
            allFiles = os.listdir()
            if file_title in allFiles:

                file_name = file_title.encode()

                f = open(file_title, "rb")
                data = f.read(BUFFER_SIZE)

                # Dosya ismi ve dosyanın yollanması

                udp_socket.sendto(file_name, addr)
                udp_socket.sendto(data, addr)

                while data:
                    if udp_socket.sendto(data, addr):
                        print("Wait...")
                        data = f.read(BUFFER_SIZE)
                        time.sleep(0.01)

                # Komut iletilme durmunun kontrolü

                try:
                    udp_socket.settimeout(3)
                    issended = udp_socket.recvfrom(BUFFER_SIZE)[0].decode()

                    if issended == "True":
                        print("Basarili gönderim...")

                except socket.timeout:

                    print("Dosya gönderilemedi hata.")

                # Socket kapatıldı

                udp_socket.close()
                f.close()

                # Eğer dosya yoksa

            else:
                udp_socket.sendto(b"error", addr)
                udp_socket.close()
        elif komut=="LIST":
            msgFromServer = str(os.listdir())
            bytesToSend = str.encode(msgFromServer)
            udp_socket.sendto(bytesToSend, addr)

        a+=1
