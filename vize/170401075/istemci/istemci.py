# Birhan Berk Oktay - 170401075

# Kullanicidan alinan get, put ve listele komutlarina gore 42. porttan ve 
# UDP uzerinden sunucu ile dosya paylasimi yapar.

# Bulundugu klasoru kullanir.

from socket import *
import sys
import select
import time
import os

def mevcutDizin():
    # Dizinde calisan python dosyasi haricinde kalan dosyalarin isimlerini
    # Alt alta string donduren fonksiyon
    dizin = os.listdir()
    a = ""
    if(sys.argv[0] in dizin):
        dizin.remove(sys.argv[0])
    for i in dizin:
        a += i + "\n"
    if(a == ""):
        a = "Dizin bos"
    return "Istemcide olan dosyalar\n-----------------------\n" + a

def dosyaVarmi(dosyaAdi):
    # Parametre olarak gelen dosya isiminin dizin icinde olup olmadigini kontrol eden
    # Varsa True yoksa False donduren fonksiyon
    dizin = os.listdir()
    if(sys.argv[0] in dizin):
        dizin.remove(sys.argv[0])
    if(dosyaAdi in dizin):
        return True
    return False

def kontrol():
    # Her bir buf kadar dosyayi gondermeden once sunucudan cevap bekleyip
    # Eğer cevap gelirse baglantinin devam ettigini anliyoruz
    # Gelmez ise baglanti dusmus demektir.
    a = 0
    while True:
        n = select.select([s], [], [], sure)
        if(n[0]):
            try:
                veri2, adres2 = s.recvfrom(buf)
                if(veri2.decode() == "basarili"):
                    return True
            except error:
                pass
        else:
            print("Sunucuya baglanmaya calisiliyor..")
            a += 1
        if(a > 1):
            return False
        
def get(dosyaAdi):
    # Get istegi yapildiginda ilk olarak dosyanin boyutunu
    # Sonrasinda ise baglantinin kontrolunu yapip dosyayi alan fonksiyon
    # Eger ilk alinan boyut ile gelen dosyanin boyutu ayni degil ise
    # Gelen eksik dosyayi siler ve hata mesaji verir
    gelmesiGerekenBoyut, adres = s.recvfrom(buf)
    gelmesiGerekenBoyut = gelmesiGerekenBoyut.decode()
    if(gelmesiGerekenBoyut == "yok"):
        print("\nSunucuda boyle bir dosya yok.\n")
    else:
        print("\nSunucudan " + dosyaAdi + " dosyasi indiriliyor. Bekleyin...")
        f = open(dosyaAdi, 'wb')
        while True:
            s.sendto("basarili".encode(), adres)
            n = select.select([s], [], [], sure)
            if(n[0]):
                veri, adres = s.recvfrom(buf)
                f.write(veri)
            else:
                f.close()
                break
        gelenBoyut = str(os.path.getsize(dosyaAdi))
        if(gelenBoyut != gelmesiGerekenBoyut):
            os.remove(dosyaAdi)
            print("Dosya alinamadi.\n")
        else:
            print("Dosya basariyla alindi.\n")

def put(dosyaAdi):
    # Istemci put istegi yaptiginda ilk olarak gonderilecek dosyanin
    # Boyutunu gonderen sonrasinda ise baglantinin kontrolunu yapip dosyayi
    # Gonderen ve buna gore gonderim bilgisini yazan fonksiyon
    hata = False
    boyut = str(os.path.getsize(dosyaAdi))
    s.sendto(boyut.encode(), adres)
    print("\nSunucuya " + dosyaAdi + " dosyasi gonderiliyor. Bekleyin...")
    f = open(dosyaAdi, "rb")
    veri = f.read(buf)
    while(veri):
        if(kontrol() == False):
            hata = True
            break
        if(s.sendto(veri, adres)):
            veri = f.read(buf)
            time.sleep(0.02)
    f.close()
    if(kontrol() == False):
        print("Dosya gonderilemedi.\n")
    else:
        print("Dosya sunucuya basariyla gonderildi.\n")

def listele():
    # Sunucudan o anki mevcut dosyalarin isimlerini alan ve
    # Istemcide bulunan dosyalari listeleyen fonksiyon
    veri, adres = s.recvfrom(buf)
    print(veri.decode())
    print(mevcutDizin())

def komutAl(secim):
    # Klavyeden girilen degere gore komutlari cagiran fonksiyon
    l = secim
    l = l.upper()
    if(l == "LISTELE" or l == "LİSTELE"):
        s.sendto(komut.encode(), adres)
        listele()
    else:
        if(len(secim) > 4):
            komutS = ""
            dosyaAdi = ""
            for i in range(len(secim)):
                if(i < 4):
                    komutS += secim[i]
                else:
                    dosyaAdi += secim[i]
            komutS = komutS.upper()
            if(komutS == "GET "):
                s.sendto(komut.encode(), adres)
                get(dosyaAdi)
            else:
                if(komutS == "PUT "):
                    if(dosyaVarmi(dosyaAdi)):
                        s.sendto(komut.encode(), adres)
                        put(dosyaAdi)
                    else:
                        print("\nDosya mevcut degil.\n")
                else:
                    print("\nGecerli bir komut giriniz.\n")
        else:
            print("\nGecerli bir komut giriniz.\n")

if(len(sys.argv) == 2): # python istemci.py sunucunun_ip_adresi seklinde calistirilmalidir
    s = socket(AF_INET, SOCK_DGRAM)
    host = sys.argv[1]
    port = 42
    buf = 4096
    adres = (host, port)
    sure = 1

    hmesaj = "Istemci baglandi"
    s.sendto(hmesaj.encode(), adres)

    # Sunucudan yanit al
    sdizin, adres = s.recvfrom(buf)
    print(sdizin.decode())
    print(mevcutDizin())
    print("Komutlar\n--------")
    print("Dosya indirmek icin -> GET dosya_adi.uzanti")
    print("Dosya yuklemek icin -> PUT dosya_adi.uzanti")
    print("Sunucudaki dosyalari listelemek icin -> LISTELE\n")
    print("Ornek -> get Manowar-Call_to_Arms_lyrics.txt")
    print("Ornek -> put Judas_Priest-Hell_Patrol.mp3")
    print("Ornek -> listele\n")
    while True:
        print("Komut gir -> ")
        komut = input()
        komutAl(komut)
else:
    print("istemci.py sunucunun_ip_adresi seklinde calistiriniz.")