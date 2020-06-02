# UĞUR ALTINTAŞ 180401067

import socket
import os
import sys
import time
import select
 
IP = str(input("Lutfen sunucu IP adresini giriniz: "))   
msgFromClient       = "ServerListele"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = (IP, 42) 
bufferSize          = 1024
 
print("Server Tarafında Bulunan Dosyalar: ")
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
ServerMesaji = UDPClientSocket.recvfrom(bufferSize)
mesaj=ServerMesaji[0].decode()

print(mesaj)
print("1- GET komutu ile sunucudan dosya indirebilirsiniz. ""GET dosyaismi.uzantı"" ")
print("2- PUT komutu ile sunucuya dosya aktarabilirsiniz. ""PUT dosyaismi.uzantı"" ")
print("3- ServerListele komutu ile sunucuda bulunan dosyaları görüntüleyebilirsiniz. ")
print("4- ClientListele komutu ile client tarafında bulunan dosyaları görüntüleyebilirsiniz. ")
print("5- exit komutu ile çıkış yapabilirsiniz.")
while True:
    
    islem=input("Yapılacak işlemi giriniz: ")
    
    if(islem == "exit"):
        break
    elif(islem[:3] == "PUT"):                                        
        
        file_name = islem[4:]
        while True:
            try:
                f = open(file_name,"rb")
            except:
                print("Dosya Bulunamadı")
                break
            UDPClientSocket.sendto(islem.encode(), serverAddressPort)
            data = f.read(bufferSize)
            while(data):
                if(UDPClientSocket.sendto(data, serverAddressPort)):
                    data = f.read(bufferSize)
                    time.sleep(0.001)
            try:
                kontrol=UDPClientSocket.recv(1024)
            except socket.error:
                print("Bağlantı hatası dosya gönderimi başarısız")
            if(kontrol.decode()=="kontrol"):
                print("Dosya başarılı bir şekilde gönderildi")
            f.close()
            break

    elif (islem[:3] == "GET"):
        UDPClientSocket.sendto(islem.encode(), serverAddressPort)
        dosya=UDPClientSocket.recv(bufferSize).decode()
        if dosya=="dosya bulunamadı":
            print("Dosya bulunamadı!")
        if dosya=="dosya bulundu":
            f = open(islem[4:],'wb')
            while True:
                ready = select.select([UDPClientSocket], [], [], 3)
                if ready[0]:
                    data= UDPClientSocket.recv(bufferSize)
                    f.write(data)
                else:
                    print("Dosya İndirildi!")
                    f.close()
                    UDPClientSocket.sendto("kontrol".encode(), serverAddressPort)
                    break
    elif (islem == "ServerListele"):
        UDPClientSocket.sendto(islem.encode(), serverAddressPort)
        dosya=UDPClientSocket.recv(bufferSize).decode()
        print("Server Tarafında Bulunan Dosyalar: ")
        print(dosya)
    elif (islem == "ClientListele"):
        listDir = os.listdir()
        print("Clitent Tarafında Bulunan Dosyalar: ")
        print(listDir)
    else:
        print('Hatali bir komut girdiniz!')


