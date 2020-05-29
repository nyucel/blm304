#Adem YILMAZ - 160401069

import socket
import os
import sys
import time




host="127.0.0.1"
port=42
adress=(host,port)
sunucuSoc=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sunucuSoc.bind(adress)

gelen=sunucuSoc.recvfrom(1024)[0].decode()
print(gelen)




while True:

    gelen2 = sunucuSoc.recvfrom(1024)[0].decode()  # gelen komut
    gelen2 = gelen2.encode()

    if(gelen2.decode()=='listele'):
        dizin=os.getcwd()
        dizin2=os.listdir(dizin)
        dizin3=[]
        for i in dizin2:
            dizin3.append(i)
        dizin4=str(dizin3)
        dizin5=dizin4.encode("utf-8")
        sunucuSoc.sendto(dizin5,adress)
        print(dizin2)
        sys.exit()
    elif (gelen2.decode() == 'put'):

        gelenIcerik = sunucuSoc.recvfrom(4096)[0].decode()
        f = open("istemciden.txt", "wb")
        f.write(gelenIcerik.encode())
        f.close()
    elif(gelen2.decode()=='get'):

        dosyaAdi,data1=sunucuSoc.recvfrom(1024)  #dosya adi geldi
        dosya=dosyaAdi.decode()
        f=open(dosya,"rb")
        data=f.read()
        f.close()
        data2=str(data)
        data3=data2.encode("utf-8")
        sunucuSoc.sendto(data3,adress)



    else:
        sys.exit()

