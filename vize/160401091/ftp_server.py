import socket
import os
import time

# Server IP ve PORT bilgisi:

IP = "localhost"
PORT = 42
bufferSize = 4096

# Server üzerinde directory oluşturulması

mainDirectory = os.listdir()
serverDirectory = "Server Directory"

if serverDirectory not in mainDirectory:
    os.mkdir(serverDirectory)
    print("Server Directory created.")
else:
    print("Directory already created. Passing...")
os.chdir(serverDirectory)


while True:

    # Bağlantının UDP üzerinden yapılabilmesi için:

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPServerSocket.bind((IP, PORT))

    i = 0

    while i < 1:

        print("Server is listening...")
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0].decode()

        address = bytesAddressPair[1]

        # Gelen komutu command: komut ve file_title: dosya adı şeklinde ayrımak için:

        command = message[:3]
        file_title = message[4:]

        # Client tarafından gelecek ilk istek directory'deki tüm dosyaları listeler

        if command == "LIST":

            msgFromServer = str(os.listdir())
            bytesToSend = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)

        # Client tarafından GET komutu yapılması durumunda:

        elif command == "GET":

            allFiles = os.listdir()

            # Eğer dosya tüm dosyalar içinde varsa:

            if file_title in allFiles:

                file_name = file_title.encode()

                f = open(file_title, "rb")
                data = f.read(bufferSize)

                # Dosya ismi ve dosyanın yollanması

                UDPServerSocket.sendto(file_name, address)
                UDPServerSocket.sendto(data, address)

                while data:
                    if UDPServerSocket.sendto(data, address):
                        print("Wait...")
                        data = f.read(bufferSize)
                        time.sleep(0.01)

                # Komut iletilme durmunun kontrolü

                try:
                    UDPServerSocket.settimeout(3)
                    issended = UDPServerSocket.recvfrom(bufferSize)[0].decode()

                    if issended == "True":
                        
                        print("Succesfully sended.")

                except socket.timeout:

                    print("Failed to send file.")

                # Socket kapatıldı

                UDPServerSocket.close()
                f.close()

            # Eğer dosya yoksa

            else:
                UDPServerSocket.sendto(b"error", address)
                UDPServerSocket.close()

        # Client tarafından PUT komutu yapılması durumunda

        elif command == "PUT":

            data = UDPServerSocket.recvfrom(bufferSize)[0]
            f = open(data.strip(), "wb")

            data = UDPServerSocket.recvfrom(bufferSize)[0]
            try:
                while data:
                    data = UDPServerSocket.recvfrom(bufferSize)[0]
                    f.write(data)

                    # Timeout bitene kadar bağlantı sağlanmasının beklenmesi

                    UDPServerSocket.settimeout(3)

            except socket.timeout:
                f.close()

            UDPServerSocket.sendto(b"True", address)
            UDPServerSocket.close()

        i += 1
