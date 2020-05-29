#Arife Oran - 160401071

import socket
import os
import time

server_ip = "127.0.0.1"
port = 42

while (True):

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((server_ip, port))
    print("IP: ", server_ip, " ", port, ".port dinleniyor")

    command,address= serverSocket.recvfrom(1024)
    cmd = command.decode()
    if ( cmd[:4] == "list"):

            fileList = str(os.listdir())
            file = fileList.encode('utf-8')
            serverSocket.sendto(file, address)

    elif (cmd[:3] == 'get'):

            files = os.listdir()
            if cmd[4:] in files:
                file_name = cmd[4:].encode('utf-8')
                f = open(cmd[4:], "rb")
                fileTransfer = f.read(1024)
                serverSocket.sendto(file_name, address)
                serverSocket.sendto(fileTransfer, address)
                try:
                    serverSocket.settimeout(1)
                    transfer, adress = serverSocket.recvfrom(1024)
                    transferSuccess = transfer.decode('utf-8')
                    if (transferSuccess == 'ISSUCCESS'):
                        print('Dosya gonderim islemi tamamamlandi')
                except socket.timeout:
                    print('Dosya gonderilirken hata olustu')
                f.close()
                serverSocket.close()
            else:
                serverSocket.sendto(b'notFound', address)
                serverSocket.close()

    elif (cmd[:3] == 'put'):

            msg, adrr = serverSocket.recvfrom(1024)
            data = msg.decode('utf-8')
            f = open(data.strip(), 'wb')
            message,adrr = serverSocket.recvfrom(1024)
            try:
                while (message):
                    message,adrr = serverSocket.recvfrom(1024)
                    f.write(message)
                    serverSocket.settimeout(1)
            except socket.timeout:
                f.close()
            serverSocket.sendto(b'SUCCESS', address)
            serverSocket.close()

