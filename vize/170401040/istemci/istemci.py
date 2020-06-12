# Medya HAN - 170401040

from socket import*
from os import system, name
import os
import time
import sys

os.chdir("istemci dosyaları")                                                               # Istemciye ait dosyaların bulundugu klasore yukseltir

def listele():                                                                              # Sunucuda bulunan dosyalari listeleyen fonksiyon

    istemciSocket.sendto(bytes("listele", encoding='utf-8'), (sunucuIP, sunucuPort))
    sunucuDosyalar = istemciSocket.recvfrom(4096)

    print("Sunucu Dosyalari Listesi: \n")
    print(sunucuDosyalar[0].decode("utf-8"))
    print("\n** Sunucu dosyalari basariyla listelenmiştir...")

def PUT(dosyaAd):

    istemciSocket.sendto(bytes("put", encoding='utf-8'), (sunucuIP, sunucuPort))            # Sunucuya hangi islemin yapilacagini bildirir
    time.sleep(1)

    if(os.path.exists(dosyaAd) == True):                                                    # PUT yapilacak dosya istemcide bulunuyorsa
        istemciSocket.sendto(bytes("bulundu", encoding='utf-8'), (sunucuIP, sunucuPort))    # Bulundugunu sunucuya bildirir
        time.sleep(1)

        istemciSocket.sendto(bytes(dosyaAd, encoding='utf-8'), (sunucuIP, sunucuPort))
        time.sleep(1)

        dosya = open(dosyaAd, "rb")                                                         # Dosyanin icerigi okunur
        dosyaIcerik = dosya.read()
        dosya.close()

        istemciSocket.sendto(dosyaIcerik, (sunucuIP, sunucuPort))

        kontrol = istemciSocket.recvfrom(4096)

        if(kontrol[0].decode("utf-8") == "tamam"):                                          # PUT yapilacak dosyayla ayni ada sahip baska bir dosya sunucuda bulunmuyorsa
            print("\n** PUT: Dosya basariyla sunucuya yuklenmistir...")
        else:                                                                               # PUT yapilacak dosyayla ayni ada sahip baska bir dosya sunucuda bulunuyorsa
            print('\nSunucu icerisinde zaten "', dosyaAd, '" adinda bir dosya var')
            print("\n1- Dosyayi uzerine yukle\n2- Dosyanin kopyasini olustur\n3- IPTAL et\n\n")

            iptal = 0
            while True:
                karar = input("Karar veriniz (1 / 2 / 3): ")

                if((karar == "1" or karar == "2")):
                    istemciSocket.sendto(bytes(karar, encoding='utf-8'), (sunucuIP, sunucuPort))
                    break
                elif(karar == "3"):
                    istemciSocket.sendto(bytes(karar, encoding='utf-8'), (sunucuIP, sunucuPort))
                    iptal = 1
                    break
                else:
                    print("\nYanlis karar.. Tekrar deneyiniz..\n")
            if(iptal == 1):                                                                 # PUT isleminden vazgecilirse
                print("\n!! Dosyanin sunucuya yuklenmesi IPTAL edildi..")
            else:
                print("\n** PUT: Dosya basariyla sunucuya yuklenmistir...")
    else:                                                                                   # PUT yapilacak dosya istemcide bulunmuyorsa
        print("\n!! Girdiginiz adda bir dosya istemcide bulunamadi..")
        istemciSocket.sendto(bytes("bulunamadi", encoding='utf-8'), (sunucuIP, sunucuPort)) # Bulunamadigini sunucuya bildirir

def GET(dosyaAd):

        istemciSocket.sendto(bytes("get", encoding='utf-8'), (sunucuIP, sunucuPort))        # Sunucuya hangi islemin yapilacagini bildirir
        time.sleep(1)

        istemciSocket.sendto(bytes(dosyaAd, encoding='utf-8'), (sunucuIP, sunucuPort))
        time.sleep(1)

        iptal = 0
        kontrol = istemciSocket.recvfrom(4096)                                              # GET yapilacak dosyanin istemcide olup olmamasi kontrolu

        if(kontrol[0].decode("utf-8") == "var"):                                            # Dosya istemcide bulunuyorsa
            dosyaIcerik, sunucuAdres = istemciSocket.recvfrom(4096)

            iptal = dosyaYukle(dosyaAd, dosyaIcerik)                                        # Hem GET isleminin iptal olup olmamasini kontrol eder
                                                                                            # Hem de dosya yukleme islemleriyle ilgili gerekli islemleri yapar
            if(iptal == 0):                                                                 # GET islemi iptal edilmezse sunucuya bunu bildirir
                istemciSocket.sendto(bytes("iptal degil", encoding='utf-8'), (sunucuIP, sunucuPort))
                print("\n** GET: Dosya basariyla istemciye yuklenmistir...")
        else:                                                                               # Dosya istemcide bulunmuyorsa
            print("\n!! Girdiginiz adda bir dosya sunucuda bulunamadi..")
        if(iptal == 1):                                                                     # GET islemi iptal edilirse
            istemciSocket.sendto(bytes("iptal", encoding='utf-8'), (sunucuIP, sunucuPort))
            print("\n!! Dosyanin istemciye yuklenmesi IPTAL edildi..")

def sonlandir():

    istemciSocket.sendto(bytes("sonlandir", encoding='utf-8'), (sunucuIP, sunucuPort))      # Sunucuya hangi islemin yapilacagini bildirir
    time.sleep(1)

    istemciSocket.close()                                                                   # Sonlandir islemi ile istemci soketi kapatilir
    print("Istemci sonlandirildi..\n")

def dosyaYukle(dosyaAd, dosyaIcerik):                                                       # GET ile dosya yukleme icin gerekli kararlarin alindigi fonksiyon

    if(os.path.exists(dosyaAd) == True):                                                   # GET yapilacak dosyayla ayni ada sahip baska bir dosya istemcide bulunuyorsa
        print('\nIstemci icerisinde zaten "', dosyaAd, '" adinda bir dosya var')
        print("\n1- Dosyayi uzerine yukle\n2- Dosyanin kopyasini olustur\n3- IPTAL et\n\n")

        while True:
            karar = int(input("Karar veriniz (1 / 2 / 3): "))
            if(karar == 1):
                dosyaYeni = open(dosyaAd, "wb")
                dosyaYeni.write(dosyaIcerik)
                dosyaYeni.close()
                break
            elif(karar == 2):                                                               # GET yapilacak dosyanin kopyasi olusturulur
                yeniAd = dosyaAd[:-4] + " (kopya)" + ".txt"
                dosyaYeni = open(yeniAd, "wb")
                dosyaYeni.write(dosyaIcerik)
                dosyaYeni.close()
                break
            elif(karar == 3):
                return 1                                                                    # GET islemini iptal edildigini dondurur
            else:
                print("\nYanlis karar.. Tekrar deneyiniz..\n")
        return 0                                                                            # GET islemini iptal edilmedigini dondurur
    else:                                                                                   # GET yapilacak dosyayla ayni ada sahip baska bir dosya istemcide bulunmuyorsa
        dosyaYeni = open(dosyaAd, "wb")
        dosyaYeni.write(dosyaIcerik)
        dosyaYeni.close()
        return 0                                                                            # GET islemini iptal edilmedigini dondurur

def clear():                                                                                # Terminal ekranini temizleme fonksiyonu

    if(name == 'nt'):
        _ = system('cls')
    else:
        _ = system('clear')


# ================================ ISTEMCI ISLEMLERI ================================ #

sunucuIP = input("\nBaglanilacak Sunucu IP: ")
sunucuPort = 42

try:
    istemciSocket = socket(AF_INET, SOCK_DGRAM)
except:
    print("!!!\nHATA: Istemci olusturma basarisiz oldu. Tekrar deneyiniz..")
    sys.exit()

istemciSocket.sendto(bytes("kontrol", encoding='utf-8'), (sunucuIP, sunucuPort))            # Sunucunun hazir olup olmadigini kontrol etmek icin

istemciSocket.settimeout(3)
try:
    kontrol = istemciSocket.recvfrom(4096)                                                  # Sunucu hazir ise mesaj yazdirilir
    print("\n** ", kontrol[0].decode("utf-8"), "\n")
except:                                                                                     # Sunucudan 3 saniye icerisinde cevap alinmazsa
    clear()
    print("\n!!!\nHATA: Sunucu hazir değil. İlk olarak sunucuyu hazir ediniz..\n")
    sys.exit()

while True:

    print("\n-------------- MENU --------------\n\n1- Listele\n2- PUT\n3- GET\n\n0- Sonlandir\n")
    secim = int(input("Secim yapiniz: "))

    if(secim == 1):
        print("\n-----------------------------------\n")
        listele()

    elif(secim == 2):
        dosyaAd = input("\n-----------------------------------\n\nPUT islemi icin dosya adini giriniz: ")

        istemciSocket.settimeout(5)
        try:
            PUT(dosyaAd)
        except:                                                                         # PUT islemi 5 saniye icerisinde gerceklesmezse
            clear()
            print("\n!!!\nHATA: Sunucu ile baglanti koptu veya başka bir hata ile karsilasildi..\nDosya sunucuya yüklenemedi. Tekrar deneyiniz..")
            sonlandir()
            break

    elif(secim == 3):
        dosyaAd = input("\n-----------------------------------\n\nGET islemi icin dosya adını giriniz: ")

        istemciSocket.settimeout(5)
        try:
            GET(dosyaAd)
        except:                                                                         # GET islemi 5 saniye icerisinde gerceklesmezse
            clear()
            print("\n!!!\nHATA: Sunucu ile baglanti koptu veya başka bir hata ile karsilasildi..\nDosya istemciye yüklenemedi. Tekrar deneyiniz..")
            sonlandir()
            break

    elif(secim == 0):
        sonlandir()
        break
    else:
        print("\nYanlis secim yaptınız. Tekrar deneyiniz..\n\n")