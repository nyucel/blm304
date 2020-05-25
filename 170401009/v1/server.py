from scapy.all import *
import time
from scapy.all import *
import time
import pickle
import os, sys
import hashlib
from pathlib import Path
from math import ceil  #dosya parça sayısını 1 yukarı yuvarlıyorum


hedef_ip =0
hedef_port=0
server_port = 42
parcalanma_boyut = 550 #bayt
dinleyici = AsyncSniffer()
gelen_paketler=[]
debug=0             # debug 1 olursa printleri açıyorum.
komut_bekle_durum=0
bekleme_zamani=0
dosya_cache={}
en_son_packet_zamani=time.time()
durum = 0







def baslangic():

        while 1:
            global bekleme_zamani
            global komut_bekle_durum
            global durum


            bekleme_zamani = 0
            komut_bekle_durum = 0
            temizlik()
            print("Dosya Transferi SUNUCUSUNA Hoşgeldiniz.")
            print("SERVER IP ADRESI =>",IP(dst="").src,"(wsl kullanılıyorsa vEthernet (WSL) adaptöründen windows üzerinden bakılmalı)")
            dinleme_baslat(alinan_paket_islemi)
            baglanti_mesaj_kontrol()
            print("bağlantı başarılı \n CLIENT IP ADRESI=",hedef_ip,"\n CLIENT DİNLEDİĞİ PORT",hedef_port)
            dinleyici.stop()
            dinleme_baslat(komut_uygula)
            komut_bekle(200)



#OLMAYAN DOSYAYI İSTEME HATASI FİXLENECEK
def komut_uygula(packet):
    global dosya_cache
    global komut_bekle_durum
    if packet.getlayer(Raw).load == "LS".encode():
        komut_ls()
        temizlik()
    if "GET".encode() in packet.getlayer(Raw).load:
        print("***********GET KOMUTU VERİLDİ*******************")
        test = packet.getlayer(Raw).load.decode().split(" ")
        print("DOSYA ADI===>>",test[1])
        hashh=hash_olustur(test[1]).hexdigest()
        print("HASH =>>>>",hashh)
        print("DOSYA BOYUTU",Path(test[1]).stat().st_size,"BAYT"," VE TAHMİNİ PARÇA SAYISI =>>>>", (Path(test[1]).stat().st_size)/parcalanma_boyut)
        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        mesaj_gonder("INF-01 "+str(test[1])+" "+str(hashh)+" "+str(Path(test[1]).stat().st_size)+" "+str(ceil((Path(test[1]).stat().st_size)/parcalanma_boyut)))
        dosya_cache=parcala_ram(test[1])
        temizlik()
        dosya_gonder()
        komut_bekle_durum = 0




def dosya_gonder():
    global dosya_cache
    global en_son_packet_zamani
    global durum
    # dinleyici.stop()
    dinleme_baslat(dosya_gonder_kontrol)
    en_son_packet_zamani=time.time()
    while len(dosya_cache)!=0:                  #Dosya parçaları atıldıkça cacheden silinir.
        for x in list(dosya_cache):
            mesaj_gonder("FILESEND "+str(x)+" "+dosya_cache[x])
            print("Kalan paket ==>",len(dosya_cache))
            if time.time() - en_son_packet_zamani > 10:
                print("DOSYA GÖNDERİMİ TİMEOUT...!!!!!!!!!!!!!!!!!!!!!!")
                dosya_cache.clear()
                return
            if durum == -1:
                print("DOSYA GÖNDERİMİNDE PROBLEM OLUŞTU.HASH UYUŞMUYOR.")
                durum = 0
                return
            if durum == 1:
                print("DOSYA GÖNDERME BAŞARILI BİR ŞEKİLDE TAMAMLANDI")
                durum = 0
                return






def dosya_gonder_kontrol(packet):
    global en_son_packet_zamani
    global dosya_cache
    global durum
    if 'OKFILE'.encode() in packet.getlayer(Raw).load:
        alinan_paket = packet.getlayer(Raw).load
        alinan_paket = alinan_paket.decode().split(" ")
        en_son_packet_zamani = time.time()  # timeout kontrolü yapıyoruz

        if int(alinan_paket[1]) in dosya_cache:  #olmayan bir değer aramayalım
            print(alinan_paket[1])
            dosya_cache.pop(int(alinan_paket[1]))  #alindiysa paket cacheden temizle paketi

    if 'FINISH_TRANSFER_ERROR'.encode() in packet.getlayer(Raw).load:
        print("HATA VAR")
        durum = -1

    if 'FINISH_TRANSFER_BASARILI'.encode() in packet.getlayer(Raw).load:
        print("DOSYA TRANSFERI BASARILI")
        durum = 1





def komut_ls():
    print("LS")
    mesaj_gonder("LS_OK! "+'\n'.join(os.listdir())) #klasör içindeki dosyaları gönderiyor.


def komut_bekle(x):
    global bekleme_zamani
    global komut_bekle_durum
    komut_bekle_durum = 1
    print("Komut Bekleniyor."+str(x)+" sn işlem yapılmazsa oturum sonlanacak")
    bekleme_zamanı= time.time()
    while komut_bekle_durum:
        print(".",end=" ")
        time.sleep(1)
        if(time.time()-bekleme_zamanı > x):
            dinleyici.stop()
            komut_bekle_durum=0





def dinleme_baslat(islem):
    global dinleyici
    temizlik()
    dinleyici=AsyncSniffer(prn=islem,filter="udp and port "+str(server_port)+"")
    dinleyici.start()
    print("PORT ==>"+str(server_port)+" Dinleniyor.")



def alinan_paket_islemi(packet):
    global hedef_ip
    global hedef_port
    # print("Paket Alındı")
    packet.show()
    if packet.getlayer(Raw) is not None :                                             #raw kısmı boş olan paketlerde aşşağıdaki satır patlıyor.Fix
        if 'Kullanici tarafindan selam!'.encode() in packet.getlayer(Raw).load:       #42 portundaki diğer şeyleri dinlemek istemiyorum.
            packet.show()
            gelen_paketler.append(packet.getlayer(Raw).load)
            hedef_ip,hedef_port = packet.getlayer(IP).src , packet.getlayer(UDP).sport      #hangi port hangi ip
            if(hedef_ip == "172.24.225.119"):
                hedef_ip="172.24.224.1"  #wsl
            mesaj_gonder("Server tarafindan selam!")

def mesaj_gonder(mesaj):
    global server_port
    global hedef_ip
    global hedef_port
    a = IP(dst=hedef_ip) / UDP(dport=hedef_port,sport=server_port) / mesaj
    #a.show()
    send(a)

def baglanti_mesaj_kontrol():
    while 1:

        if "Kullanici tarafindan selam!".encode() in gelen_paketler:  #server tarafindan mesaj geldi mi ?
            temizlik()
            return 1
        # mesaj_gonder("Server tarafindan selam!")
        print(".",end=" ")
        time.sleep(1)                                               #çok hızlı olursa paket kaçırıyor.





""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""        YARDIMCILAR          """""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""


def parcala_ram(fromfile, chunksize=parcalanma_boyut):  #dosyaları parçalanma boyutuna kadar chunklar halinde rame bir dizi şeklinde depoluyor.
    partnum = 0
    input = open(fromfile, 'rb')                   # use binary mode on Windows
    geri_donecek_dosya={}
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        filename = partnum

        geri_donecek_dosya[filename]=chunk.hex()  #DOSYANUMARASI BOŞLUK CHUNK un hex hali (byte normalde)
        # fileobj  = open(filename, 'wb')
        # fileobj.write(chunk)
        # fileobj.close()                            # or simply open(  ).write(  )
    input.close()
    return geri_donecek_dosya



def hash_olustur(file):
    file_hash = hashlib.blake2b() #b2sum
    with open(file, "rb") as f:
        while 1:
            chunk = f.read(8192)
            if not chunk:
                break
            file_hash.update(chunk)
            f.read(8192)
        f.close()
    return file_hash

def temizlik():
    f = open("logs_file","ab+")
    pickle.dump(gelen_paketler,f)
    f.close()
    gelen_paketler.clear()          #paketleri temizleyelim.


if __name__ == "__main__":
    baslangic()