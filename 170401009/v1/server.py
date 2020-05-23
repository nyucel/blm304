from scapy.all import *
import time
from scapy.all import *
import time
import pickle
import os, sys


hedef_ip =0
hedef_port=0
server_port = 42
parcalanma_boyut = 0
dinleyici = AsyncSniffer()
gelen_paketler=[]
debug=0             # debug 1 olursa printleri açıyorum.
komut_bekle_durum=0
bekleme_zamani=0









def baslangic():

        while 1:
            global bekleme_zamani
            global komut_bekle_durum


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
            komut_bekle()



def komut_uygula(packet):
    if packet.getlayer(Raw).load == "LS".encode():
        komut_ls()
        temizlik()



def komut_ls():
    print("LS")
    mesaj_gonder("LS_OK! "+'\n'.join(os.listdir())) #klasör içindeki dosyaları gönderiyor.


def komut_bekle():
    global bekleme_zamani
    global komut_bekle_durum
    komut_bekle_durum = 1
    print("Komut Bekleniyor.10 sn işlem yapılmazsa oturum sonlanacak")
    bekleme_zamanı= time.time()
    while komut_bekle_durum:
        print(".",end=" ")
        time.sleep(1)
        if(time.time()-bekleme_zamanı > 10):
            dinleyici.stop()
            komut_bekle_durum=0





def dinleme_baslat(islem):
    global dinleyici
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






def temizlik():
    f = open("logs_file","ab+")
    pickle.dump(gelen_paketler,f)
    f.close()
    gelen_paketler.clear()          #paketleri temizleyelim.


if __name__ == "__main__":
    baslangic()