# Medya HAN - 170401040

from socket import*
import os
import time
import sys

# ================================ SUNUCU ISLEMLERI ================================ #

os.chdir("sunucu dosyaları")                                                                # Sunucuya ait dosyaların bulundugu klasore yukseltir

sunucuIP = '127.0.0.1'
sunucuPort = 42

try:
    sunucuSocket = socket(AF_INET, SOCK_DGRAM)
    sunucuSocket.bind((sunucuIP, sunucuPort))
except:
    print("!!!\nHATA: Sunucu olusturma basarisiz oldu. Tekrar deneyiniz..")
    sys.exit()

print("\n------- Sunucu hazir durumda -------\n")

kontrol, istemciAdres = sunucuSocket.recvfrom(4096)
sunucuSocket.sendto(bytes("Sunucuya baglanildi..", encoding='utf-8'), istemciAdres)         # Sunucu hazir ise istemciye mesaj gonderilir

while True:
    islem, istemciAdres = sunucuSocket.recvfrom(4096)                                       # Istemcide istenen islem bilgisini alir

    print("\n------------------------------------\n\nIstemciden islem bilgisi alindi: ", islem.decode("utf-8"))

    if(islem.decode("utf-8") == "listele"):
        dosyalar = "\n".join(os.listdir())                                                  # Sunucudaki dosyalar "dosyalar" adli degiskene string olarak atanir
        sunucuSocket.sendto(bytes(dosyalar, encoding='utf-8'), istemciAdres)                # Listelenecek dosyalar istemciye gonderilir
        print("\nListelenecek dosyalar istemciye gonderildi..")

    elif(islem.decode("utf-8") == "put"):
        bilgi = sunucuSocket.recvfrom(4096)                                                 # PUT yapilacak dosyanin istemcide bulunup bulunmama bilgisi alinir

        if(bilgi[0].decode("utf-8") == "bulundu"):                                          # PUT yapilacak dosya istemcide bulunuyorsa
            dosyaAd, istemciAdres = sunucuSocket.recvfrom(4096)

            dosyaIcerik = sunucuSocket.recvfrom(4096)

            if(os.path.exists(dosyaAd.decode("utf-8")) == True):                           # PUT yapilacak dosyayla ayni ada sahip baska bir dosya sunucuda bulunuyorsa
                sunucuSocket.sendto(bytes("aynisi var", encoding='utf-8'), istemciAdres)

                iptal = 0

                karar = sunucuSocket.recvfrom(4096)                                         # PUT ile dosya yukleme icin verilen karari istemciden alir

                if(karar[0].decode("utf-8") == "1"):
                    dosyaYeni = open(dosyaAd, "wb")
                    dosyaYeni.write(dosyaIcerik[0])
                    dosyaYeni.close()
                elif(karar[0].decode("utf-8") == "2"):                                     # PUT yapilacak dosyanin kopyasi olusturulur
                    yeniAd = dosyaAd.decode("utf-8")[:-4] + " (kopya)" + ".txt"
                    dosyaYeni = open(yeniAd, "wb")
                    dosyaYeni.write(dosyaIcerik[0])
                    dosyaYeni.close()
                elif(karar[0].decode("utf-8") == "3"):                                     # PUT islemi iptal edilirse "iptal" degiskeni 1 yapilir
                    iptal = 1

                if(iptal == 0):
                    print("\nPUT islemi basariyla gerceklesti..")
                else:                                                                       # PUT islemi iptal edilirse
                    print("\n!! PUT islemi IPTAL edildi..")
            else:                                                                           # PUT yapilacak dosyayla ayni ada sahip baska bir dosya sunucuda bulunmuyorsa
                dosyaYeni = open(dosyaAd, "wb")
                dosyaYeni.write(dosyaIcerik[0])
                dosyaYeni.close()
                sunucuSocket.sendto(bytes("tamam", encoding='utf-8'), istemciAdres)
                print("\nPUT islemi basariyla gerceklesti..")
        else:                                                                               # PUT yapilacak dosya istemcide bulunmuyorsa
            print("\n! Girilen adda bir dosya istemcide bulunamadi..")

    elif(islem.decode("utf-8") == "get"):
        dosyaAd, istemciAdres = sunucuSocket.recvfrom(4096)

        if os.path.exists(dosyaAd.decode("utf-8")) == True:                                 # GET yapilacak dosya sunucuda bulunuyorsa
            time.sleep(1)
            sunucuSocket.sendto(bytes("var", encoding='utf-8'), istemciAdres)               # Dosyanin sunucuda bulundugu bilgisi istemciye gonderilir

            dosya = open(dosyaAd.decode("utf-8"), "rb")
            dosyaIcerik = dosya.read()
            dosya.close()

            time.sleep(1)
            sunucuSocket.sendto(dosyaIcerik, istemciAdres)

            kontrol = sunucuSocket.recvfrom(4096)                                           # GET isleminin iptal edilip edilmedigi bilgisini istemciden alir

            if(kontrol[0].decode("utf-8") == "iptal"):                                      # GET islemi iptal edilirse
                print("\n!! GET islemi IPTAL edildi..")
            else:
                print("\nGET islemi basariyla gerceklesti..")
        else:                                                                               # GET yapilacak dosya sunucuda bulunmuyorsa
            time.sleep(1)
            sunucuSocket.sendto(bytes("yok", encoding='utf-8'), istemciAdres)
            print("\n! Girilen adda bir dosya sunucuda bulunamadi..")

    elif(islem.decode("utf-8") == "sonlandir"):
        print("\nSonlandirma mesaji alindi.. Sunucu kapaniyor..")
        sunucuSocket.close()                                                                # Sonlandir islemi ile sunucu soketi kapatilir
        print("\n---------- Sunucu kapandi ----------")
        break