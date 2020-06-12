import socket
import time
import os
import scapy
sunucuSocket_ip="127.0.0.1"
sunucuSocket_port=42
#BAHAR ÇİFTÇİ                    #BAHAR ÇİFTÇİ
sunucuSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #sock_dgram udp ile haberleşmek için
sunucuSocket.bind((sunucuSocket_ip,sunucuSocket_port))
veri, clientAdres= sunucuSocket.recvfrom(4096) 
print(veri.decode('utf-8'))

msg="Sunucu, baglantiyi baslatti.. istemci sunucuya baglandi.."
mesaj=msg.encode('utf-8')
sunucuSocket.sendto(mesaj,clientAdres)
print("Baglanti gerçekleşti..")

#BAHAR ÇİFTÇİ                             #BAHAR ÇİFTÇİ
def putIslemi():
        data2, clientAdres=sunucuSocket.recvfrom(4096)
        gelen2=data2.decode('utf-8')
        if(gelen2=="dosya mevcut"):
            dosya= open(gelen_secim,"wb")
            paket_sayisi , clientAdres = sunucuSocket.recvfrom(4096)
            sayim=paket_sayisi.decode('utf8')
            sayim2=int(sayim)
            while sayim2 != 0:
                data_general , clientAdres = sunucuSocket.recvfrom(4096)
                dosya_verisi= dosya.write(data_general)
                sayim2= sayim2 - 1
                dosya.close()
            print("put islemi basariyla tamamlandi..\n")
        else:
            print(gelen2+"\n")
def getIslemi(gelen_dosya):
    path='/Users/hp/Desktop/server/serverFiles'+ str(gelen_dosya)
    if os.path.isfile(path):
        msg="dosya mevcut"
        mesaj=msg.encode('utf-8')
        sunucuSocket.sendto(mesaj,clientAdres)
        dosya_durumu=os.stat(path)
        dosya_boyutu=dosya_durumu.st_size 
        boyut_hesapla=int(dosya_boyutu / 4096) 
        boyut_hesapla= boyut_hesapla +1  
        durum=str(boyut_hesapla) 
        durum2=durum.encode('utf8')
        sunucuSocket.sendto(durum2,clientAdres)
        kontrol_boyut = int(boyut_hesapla)
        dosya = open(path,"rb") 
        while kontrol_boyut != 0:
            dosya2=dosya.read(4096) 
            sunucuSocket.sendto(dosya2,clientAdres)
            kontrol_boyut = kontrol_boyut - 1
        dosya.close()
        print("get islemi basariyla tamamlandi..\n")
    else:
        msg="Dosya adini hatali girdiniz yada dosya mevcut degil\n"
        mesaj=msg.encode('utf-8')
        sunucuSocket.sendto(mesaj, clientAdres)

def listIslemi():
    print("Listeleme fonksiyonu calistirildi..\n")
    X = os.listdir(path="C:/Users/hp/Desktop/server/serverFiles")
    liste = []
    for kopya_dosya in X:
        liste.append(kopya_dosya)
    liste_string= str(liste)
    liste_islem =liste_string.encode('utf-8')
    sunucuSocket.sendto(liste_islem,clientAdres)
    print("Sunucu dosyalari listeledi..\n")

def exitConnection():
    gelen_mesaj , clientAdres=sunucuSocket.recvfrom(4096)
    metin=gelen_mesaj.decode('utf-8')
    print(metin+"\n")
    msg="baglanti sonlandirildi.."
    mesaj=msg.encode('utf-8')
    sunucuSocket.sendto(mesaj,clientAdres)
    sunucuSocket.close()

def serverError():
    msg="Hata olustu - girdiginiz '" + gelen_secim + "'komutu sistem icinde mevcut degil.. lütfen dogru oldugundan emin olun!\n"
    mesaj=msg.encode('utf-8')
    sunucuSocket.sendto(mesaj, clientAdres)
    print("Hatali islem!.\n")


while True:
    data, clientAdres = sunucuSocket.recvfrom(4096)
    gelen_secim=data.decode('utf-8')
    if(gelen_secim=="put"):
        putIslemi()
    elif(gelen_secim=="get"):
        data2, clientAdres=sunucuSocket.recvfrom(4096)
        gelen2=data2.decode('utf-8')
        getIslemi(gelen2)
    elif(gelen_secim=="list"):
        listIslemi()
    elif (gelen_secim=="exit"):
        exitConnection()
        break
    else:
        serverError()
