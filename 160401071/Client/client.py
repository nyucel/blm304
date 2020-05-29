#Arife Oran - 160401071

import socket
import os
import sys
import time

ip = input("Baglanmak istediginiz sunucunun IP adresini girin:\n")
serverAddr = (ip, 42)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cmd = "list"
cmdList = cmd.encode('utf-8')
try:
    clientSocket.sendto(cmdList, serverAddr)

except:
    print('Baglanti hatasi')
    sys.exit()

message, addr = clientSocket.recvfrom(1024)
msg = message.decode('utf-8')
newMessage = "Erisim izniniz olan dosyalar: {}".format(msg)
print(newMessage)

command = input("Dosya Indirebilmek icin : get dosya_adi\nDosya gonderimi icin: put dosya_adi")
cmd = command.encode('utf-8')
clientSocket.sendto(cmd, serverAddr)

if (command.find('get') == 0):

    fileTransfer,adress = clientSocket.recvfrom(1024)
    if (fileTransfer.decode('utf-8') == 'notFound'):
        print('Dosya bulunamadi')
    else:
        f = open(fileTransfer.strip(), 'wb')
        fileTransfer,adress = clientSocket.recvfrom(1024)
        try:
            while (fileTransfer):
                fileTransfer,adress = clientSocket.recvfrom(1024)
                f.write(fileTransfer)

                clientSocket.settimeout(1)
        except socket.timeout:
            f.close()
        clientSocket.sendto(b'ISSUCCESS', serverAddr)
        clientSocket.close()

elif(command.find('put') == 0):
    fileList = os.listdir()
    if command[4:] in fileList:
        file = command[4:].encode('utf-8')
        f = open(command[4:], "rb")
        putFile = f.read(1024)
        clientSocket.sendto(file, serverAddr)
        clientSocket.sendto(putFile, serverAddr)
        try:
            clientSocket.settimeout(1)
            data,adress = clientSocket.recvfrom(1024)
            isPut = data.decode('utf-8')
            if (isPut == 'SUCCESS'):
                print('Dosya gonderildi')
        except socket.timeout:
            print('Dosya gonderimi basarisiz')
        f.close()
        clientSocket.close()
    else:
        print('Dosya bulunamadi')
        sys.exit()
else:
    print('Hatali giris yaptiniz lütfen tekrar deneyiniz.')
