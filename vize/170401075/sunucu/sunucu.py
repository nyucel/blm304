# Birhan Berk Oktay - 170401075

# Istemcinin get, put ve listele komutlarina gore 42. porttan ve 
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
    return "\nSunucuda olan dosyalar\n-----------------------\n" + a

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
            a += 1
        if(a>3):
            return False

def get(dosyaAdi):
    # Istemciden get istegi yaptiginda ilk olarak gonderilecek dosyanin 
    # Boyutunu gonderen sonrasinda ise baglantinin kontrolunu yapip dosyayi
    # Gonderen ve buna gore gonderim bilgisini yazan fonksiyon
    hata = False
    boyut = str(os.path.getsize(dosyaAdi))
    s.sendto(boyut.encode(), adres)
    print("Istemciye " + dosyaAdi + " dosyasi gonderiliyor.")
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
    if(hata == True):
        print("Dosya gonderilemedi\n")
    else:
        print("Dosya istemciye basariyla gonderildi.\n")

def put(dosyaAdi):
    # Istemci put istegi yaptiginda ilk olarak dosyanin boyutunu
    # Sonrasinda ise baglantinin kontrolunu yapip dosyayi alan fonksiyon
    # Eger ilk alinan boyut ile gelen dosyanin boyutu ayni degil ise
    # Gelen eksik dosyayi siler ve hata mesaji verir
    # Islem tamamlandiktan sonra sunucudaki dosyalari ekrana yazdirir
    gelmesiGerekenBoyut, adres = s.recvfrom(buf)
    gelmesiGerekenBoyut = gelmesiGerekenBoyut.decode()
    print("Istemci " + dosyaAdi + " dosyasini yukluyor.")
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
    print(mevcutDizin())

def listele():
    # Istemciye o an sunucunun dizininde bulunan dosyalari gonderen fonksiyon
    dizin = mevcutDizin()
    s.sendto(dizin.encode(), adres)

def komutAl(secim):
    # Kullanicidan alinan input a gore ilgili fonksiyonu cagiran fonksiyon
    l = secim
    l = l.upper()
    if(l == "LISTELE" or l == "LİSTELE"):
        listele()
    else:
        if(len(secim) > 4):
            komut = ""
            dosyaAdi = ""
            for i in range(len(secim)):
                if(i < 4):
                    komut += secim[i]
                else:
                    dosyaAdi += secim[i]
            komut = komut.upper()
            if(komut == "GET "):
                if(dosyaVarmi(dosyaAdi)):
                    get(dosyaAdi)
                else:
                    m = "yok"
                    s.sendto(m.encode(), adres)
            if(komut == "PUT "):
                put(dosyaAdi)

s = socket(AF_INET, SOCK_DGRAM)
host = ""
port = 42
buf = 4096
s.bind((host, port))
sure = 1

print(host)
print(mevcutDizin())

# Karsilama kismi
hveri, adres = s.recvfrom(buf)
hmesaj = "\n---------------Sunucuya hos geldin---------------\n\n" + mevcutDizin()
s.sendto(hmesaj.encode(), adres)

# Komut alma kismi
while True:
    veri, adres = s.recvfrom(buf)
    komutAl(veri.decode())
