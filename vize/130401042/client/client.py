import socket
import os
import time
import sys               ##BAHAR ÇİFTÇİ
import scapy
istemciSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
    ip=input("Sunucu ip'sini giriniz :  ")
    if(ip=="127.0.0.1"):
        break
    else:
        print("Hatali veya yanlis sunucu ip adresi girdiniz\n")
#BAHAR ÇİFTÇİ                       #BAHAR ÇİFTÇİ
msg="istemci, sunucu ile baglanti kurmak istiyor?"
mesaj=msg.encode('utf-8')
istemciSocket.sendto(mesaj,(ip,42)) #42. port haberleşiyorlar

data , sunucuAdres = istemciSocket.recvfrom(4096)
print(data.decode('utf-8')+"\n")

while True:
    islem = input("\nNe yapmak istiyorsunuz ? : (1-Dosya yüklemek) put  (2-Dosya indirmek) get (3-Dosya listelemek) list  (4-Baglantiyi kesmek) exit      :   ")
    secilen=islem.encode('utf-8')
    istemciSocket.sendto(secilen, sunucuAdres)
    if(islem=="put"):
        dosyaSec=input("\nLütfen dosya adını dogru şekilde giriniz : ")
        path="/Users/hp/Desktop/client/clientFiles/" + str(dosyaSec)
        if os.path.isfile(path):
            msg="dosya mevcut"
            mesaj=msg.encode('utf-8')
            istemciSocket.sendto(mesaj,sunucuAdres)
            dosya_boyut=os.stat(path)
            boyut_devam=dosya_boyut.st_size
            paket_sayisi=int(boyut_devam / 4096)
            paket_sayisi = paket_sayisi +1
            devamEt=str(paket_sayisi)
            devamEt2=devamEt.encode('utf8')
            istemciSocket.sendto(devamEt2,sunucuAdres)
            devam_kosul=int(paket_sayisi)
            dosya = open(path, "rb")
            while devam_kosul != 0:
                acDosya = dosya.read(4096)
                istemciSocket.sendto(acDosya,sunucuAdres)
                devam_kosul= devam_kosul -1
            dosya.close()
            print("Dosya upload edildi sunucu dizinini kontrol edebilirsiniz..\n")
        else:
            msg="dosya mevcut degil"
            istemciSocket.sendto(msg.encode('utf-8'),sunucuAdres)
            print("Dosya adını hatali yada yanlis girdiniz.!")
    elif(islem=="get"):
        dosyaSec=input("\nLütfen dosya adını dogru sekilde giriniz : ")
        dosya=dosyaSec.encode('utf-8')
        istemciSocket.sendto(dosya,sunucuAdres)
        gelen_yanit, sunucuAdres = istemciSocket.recvfrom(4096)
        yanit=gelen_yanit.decode('utf-8')
        if(yanit=="dosya mevcut"):
            gelen_paket= open("Received olan dosya-" +dosyaSec,"wb")
            paket_numarasi, sunucuAdres = istemciSocket.recvfrom(4096)
            mevcut_paket=paket_numarasi.decode('utf-8')
            paket_durum=int(mevcut_paket)
            while paket_durum != 0: 
                data2, sunucuAdres = istemciSocket.recvfrom(4096)
                data_process=gelen_paket.write(data2)
                paket_durum= paket_durum -1
            gelen_paket.close()
            print("Dosya alindi sunucu dizinine bakabilir yada list komutunu calistirabilirsiniz\n")
        else:
            print(yanit+"\n")
    elif(islem=="list"):
        data, sunucuAdres = istemciSocket.recvfrom(4096) #alınan veri boyutu 4096 bayt
        gelen_dosyalar = data.decode('utf-8')
        print(gelen_dosyalar+"\n")
        print("Sunucu dosyalari listeledi..\n")
    elif(islem=="exit"):
        msg="Mesaj : istemci baglantiyi sonlandirmak istiyor"
        mesaj=msg.encode('utf-8')
        istemciSocket.sendto(mesaj,sunucuAdres)
        gelen_mesaj , sunucuAdres = istemciSocket.recvfrom(4096)
        mesaj=gelen_mesaj.decode('utf-8')
        print(mesaj+"\n")
        istemciSocket.close()
        break
    else:
        gelen_mesaj, sunucuAdres = istemciSocket.recvfrom(4096)
        mesaj=gelen_mesaj.decode('utf-8')
        print(mesaj+"\n")
