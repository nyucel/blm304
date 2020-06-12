#Zeliha Döner 160401004
import socket
import sys
import os
import time
import select
from socket import timeout

#c_ip="127.0.0.1"
c_port=42
c_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c_ip=str(input("İp adresini giriniz: "))
buf=1024

#istemci ip adresi girerek oturum açar
while 1:
    if c_ip == "127.0.0.1":
        print("Oturum açıldı")
        break
    else:
        print("Doğru ip adresini girmediniz.!")
    c_ip=str(input("İp adresini giriniz: "))   

while True:
    command=input("Lütfen komut girin: \n1. listele\n2. get \n3. put \n4. exit\n")
    CommClient = command.encode('utf-8')
    c_s.sendto(CommClient, (c_ip, c_port))
    CL = command.split()

    #sunucuda dosya listelenir
    if CL[0] == "listele":
        ClientData, clientAddr = c_s.recvfrom(51200)
        text = ClientData.decode('utf8')
        print(text)
        if text == "Liste getir komutu":
            ClientDataL, clientAddrL = c_s.recvfrom(4096)
            text2 = ClientDataL.decode('utf8')
            print(text2)
        else:
            print("Error. Invalid.")

    #istemci get komutu ile sunucudan dosya indirir       
    elif CL[0]== "get":
        filename=input("Dosya adını giriniz:")
        ffilename=filename.encode('utf-8')
        c_s.sendto(ffilename,(c_ip, c_port))
        data, addr = c_s.recvfrom(1024)
        dosya=open(filename,"wb")
        dosya.write(data)
        dosya.close()
        
    #istemci put komutu ile sunucuya dosya yükler
    elif CL[0]== "put":
        file_name = input("Dosya adı giriniz:")
        ffilename=file_name.encode('utf-8')
        if os.path.exists(file_name)==True:
            c_s.sendto(ffilename, (c_ip, c_port))
            print ("%s gönderiliyor..." % file_name)
            f = open(file_name, "r")
            data = f.read(buf)
            while(data):
                if(c_s.sendto(data, (c_ip, c_port))):
                    data = f.read(buf)
                    time.sleep(0.02)
            f.close()
        else:
            print("Dosya yüklenemedi")
            c_s.close()

    elif CL[0]== "exit":
        c_s.close()
        break