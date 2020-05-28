import socket
import os
import sys
import time

# Server IP ve PORT bilgisi:

IP = "10.0.2.4"
PORT = 42

serverAddressPort = (IP, PORT)
bufferSize = 4096

msgFromClient = "LIST"
bytesToSend = str.encode(msgFromClient)

# Bağlantının UDP üzerinden yapılabilmesi için:

UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:

    #  Dosyaların listelenmesi için ilk olarak LIST komutunu gönderiyoruz:

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

except:

    #  Exception:

    print("Can't connect to server.")
    sys.exit()

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Files {}".format(msgFromServer[0].decode())

print(msg)

#  Kullanıcıdan girdi alma:

command = input(
    "You can use the command line to use FTP server: 'COMMAND (PUT / GET) FILE_NAME'"
)

command = command.encode()
UDPClientSocket.sendto(command, serverAddressPort)

# GET komutu yapılması durumunda:

if command.find("GET") == 0:

    data = UDPClientSocket.recvfrom(bufferSize)[0]

    #  Eğer dosya bulunamazsa

    if data.decode() == "error":
        print("Not found.")

    #  Eğer dosya bulunması durumunda

    else:
        f = open(data.strip(), "wb")

        data = UDPClientSocket.recvfrom(bufferSize)[0]

        try:
            while data:
                data = UDPClientSocket.recvfrom(bufferSize)[0]
                f.write(data)

                # Timeout bitene kadar bağlantı sağlanmasının beklenmesi

                UDPClientSocket.settimeout(3)

        except socket.timeout:

            f.close()

        UDPClientSocket.sendto(b"True", serverAddressPort)
        UDPClientSocket.close()

# PUT komutu yapılması durumunda:

elif command.find("PUT") == 0:

    #  Dosyanın isminin alınması:

    file_title = command[4:]
    allFiles = os.listdir()

    # Dosya varsa:

    if file_title in allFiles:

        file_name = file_title.encode()

        f = open(file_title, "rb")

        data = f.read(bufferSize)

        # Dosya ismi ve dosyanın yollanması

        UDPClientSocket.sendto(file_name, serverAddressPort)
        UDPClientSocket.sendto(data, serverAddressPort)

        while data:
            if UDPClientSocket.sendto(data, serverAddressPort):
                print("Sending...")
                data = f.read(bufferSize)
                time.sleep(0.01)

        try:

            # Timeout bitene kadar bağlantı sağlanmasının beklenmesi

            UDPClientSocket.settimeout(3)
            kontrol = UDPClientSocket.recvfrom(bufferSize)[0].decode()

            if kontrol == "True":

                print("File successfully sended.")

        except socket.timeout:

            print("Failed to send file.")

        UDPClientSocket.close()
        f.close()

    else:
        print("Not found.")

else:
    print("Please enter a command which is GET or PUT.")
