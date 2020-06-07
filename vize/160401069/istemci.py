#Adem YILMAZ - 160401069

import socket
import os
import sys
import time

host=input("Baglanti icin IP numarasi giriniz(127.0.0.1 olarak giriniz)=")
port=42
buffer=4096
adress=(host,port)

if host=='127.0.0.1':
    print("IP numarasi dogru baglanti kuruluyor.")
    time.sleep(3)
else:
    print("Ip numarasini yanlis girdiniz tekrar deneyiniz.")
    sys.exit()
istemciSoc=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
mesaj="BAGLANTI BASARILI"
mesaj=mesaj.encode("utf-8")
istemciSoc.sendto(mesaj,adress)
while True:
    yapilacakIslem=input("Yapmak istediginiz islemi seciniz\n*Listelemek icin 'listele'\n*GET icin 'get dosyaismi'\n*PUT icin 'put'\nCıkıs icin exit\nolarak giriniz=")
    islem=yapilacakIslem.split()

    if(islem[0]=='listele'):

        islem1=islem[0].encode("utf-8")
        istemciSoc.sendto(islem1,adress)
        gelen=istemciSoc.recvfrom(buffer)[0].decode()
        print(gelen)

    elif (islem[0] == 'put'):
        islemPut=islem[0].encode("utf-8")
        istemciSoc.sendto(islemPut,adress)
        yuklenecekDosya = 'istemciden.txt'  #put islemi yaparken istemcinin bulunduğu dizindeki dosyayı manuel tanımladım
        f = open(yuklenecekDosya, "rb")
        icerik = (f.read()).decode("utf-8")
        f.close()
        icerik = str.encode(icerik)
        istemciSoc.sendto(icerik, adress)
    elif(islem[0]=='get'):


        mesajG=str(islem[0]).encode()
        istemciSoc.sendto(mesajG,adress)
        try:
            deneme=islem[1]
            islem2=str(islem[1])
            islem3=islem2.encode()
            istemciSoc.sendto(islem3,adress)
            gelen= istemciSoc.recvfrom(1024)[0].decode()
            f1 = open(islem2, "wb")
            f1.write(gelen)
            f1.close()
        except:
            print("Bir hata var")
    elif(islem[0]=='exit'):
        cikis=islem[0].encode()
        istemciSoc.sendto(cikis,adress)
        sys.exit()
    else:
        print(islem,"yanlistir. Lutfen get dosyaadi.txt/put/listele bunlardan birini yaziniz")
