#Mehmet Salih ÇELİK - 170401073
import socket
import os
import sys
import time

sunucu_port=42
buffer=32768
#buffer boyutum 32KB
istemci_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
istemci_socket.settimeout(3)
#baglanti kontrolu icin sure 3 saniye



def decode_yap(x):
    return x.decode("utf-8")

def encode_yap(x):
    return x.encode("utf-8")


###Sunucu baglantisi ve sunucu_dosyalari klasorunu ekrana yazdirma islemi
while 1:
    sunucu_ip=str(input("Baglanilmak istenen sunucu ip sini giriniz : "))
    sunucu = (sunucu_ip, sunucu_port)
    mesaj=""
    mesaj=encode_yap(sunucu_ip)
    try:
        istemci_socket.sendto(mesaj,sunucu)
        yenimesaj,sunucu_ip=istemci_socket.recvfrom(buffer)
        yenimesaj=decode_yap(yenimesaj)
    except:
        print("Hatali ip girisi yapildi veya sunucudan yanit alinamiyor.")
        a=str(input("Yeniden denemek icin 1 , cikmak icin herhangi bir tusa basin : "))
        if a=="1":
            continue
        else:
            break

    print("BAGLANTI BASARILI \n")
    print(yenimesaj)
    sunucudaki_dosyalar=yenimesaj
    istemcideki_dosyalar=os.listdir("istemci_dosyalari")

### Burada kullanici dogru komut girmis mi veya dogru dosya adi girmis mi kontrolu yapiyorum.
    mesaj = str(input("--- Yapilmak istenen islemi, dosya ismini ve uzantisini yaziniz.(GET abc.jpg , PUT xyz.txt) --- \n"))
    if mesaj[:3] != "GET" and mesaj[:3] != "PUT":
        print("Yanlis komut kullandiniz...")
        a = str(input("Menuye donmek icin 1 , cikmak icin herhangi bir tusa basin : "))
        if a == "1":
            mesaj = encode_yap("1")
            istemci_socket.sendto(mesaj, sunucu)
            continue
        else:
            mesaj=encode_yap(mesaj)
            istemci_socket.sendto(mesaj, sunucu)
            break
    elif mesaj[:3]=="GET" and mesaj[4:] in sunucudaki_dosyalar:
        mesaj2 = encode_yap(mesaj)
        istemci_socket.sendto(mesaj2, sunucu)

    elif mesaj[:3]=="PUT" and mesaj[4:] in istemcideki_dosyalar:
        mesaj2 = encode_yap(mesaj)
        istemci_socket.sendto(mesaj2, sunucu)
    else:
        print("Olmayan bir dosya adi girdiniz...")
        a = str(input("Menuye donmek icin 1 , cikmak icin herhangi bir tusa basin : "))
        if a == "1":
            mesaj = encode_yap("1")
            istemci_socket.sendto(mesaj, sunucu)
            continue
        else:
            mesaj=encode_yap(mesaj)
            istemci_socket.sendto(mesaj, sunucu)
            break

###Sunucudan dosya boyutunu mesaj olarak alıyoruz.Dosya boyutu kadar byte'ı indirme islemi yapıyoruz ve aynı isimde bir dosya olusturup byte'ları yazıyoruz.
    if mesaj[:3]=="GET":
        veri, sunucu_ip = istemci_socket.recvfrom(buffer)
        dosya_boyutu=decode_yap(veri)
        print("indirilecek dosya boyutu : ",dosya_boyutu,"byte")
        f = open("istemci_dosyalari/"+mesaj[4:], "wb")
        boyut_kontrol = 0
        while True:
            if ((boyut_kontrol*buffer)<int(dosya_boyutu)):
                try:
                    yenimesaj, sunucu_ip = istemci_socket.recvfrom(buffer)
                except:
                    print("SUNUCUYLA OLAN BAGLANTI KESILDI.SUNUCUYU YENIDEN CALISTIRIN")
                    f.close()
                    break
                else:
                    f.write(yenimesaj)
                    print("Dosya aliniyor...")
                    boyut_kontrol+=1
            else:
                f.close()
                print("DOSYA ALINDI.")
                break
        a=str(input("Menuye donmek icin 1 , cikmak icin herhangi bir tusa basin : "))
        if a=="1":
            continue
        else:
            break
## Dosyayı gonderirken serverdaki yazma hızı problem olusturmasın diye time.sleep(0.3) yazdık ve her paket gonderme islemi icin 300milisaniye beklettik.
    if mesaj[:3]=="PUT":
        f=open("istemci_dosyalari/"+mesaj[4:],"rb")
        dosya_boyutu=encode_yap(str(os.stat("istemci_dosyalari/"+mesaj[4:])[6]))
        istemci_socket.sendto(dosya_boyutu,sunucu)
        veri=f.read(buffer)
        boyut_kontrol=1
        while veri:
            try:
                control, sunuc_ip = istemci_socket.recvfrom(buffer)
            except:
                print("SUNUCUYLA OLAN BAGLANTI KESILDI . SUNUCUYU YENIDEN CALISTIRIN")
                f.close()
                break
            else:
                istemci_socket.sendto(veri, sunucu)
                print("Dosya yollaniyor...")
                veri=f.read(buffer)
                time.sleep(0.3)
                boyut_kontrol+=1
        if (buffer*boyut_kontrol) >= int(dosya_boyutu):
            print("YOLLANDI.")
            f.close()

        a = str(input("Menuye donmek icin 1 , cikmak icin herhangi bir tusa basin : "))
        if a == "1":
            continue
        else:
            break



istemci_socket.close()