#!/usr/bin/env python
# -*- coding: utf-8 -*-

#scapy kullanmaya karar vermiştim fakat. Tcp bağlantısında kernel üzerinden
#yapmıyormuş. ve sorunlar ortaya çıktı o yüzden socket ile yapmaya karar verdim.
#1 second =1000 milliseconds
#time.time() fonksiyonu saniye cinsinden veriyor.

# from scapy.all import * #sadece makine ip sini öğrenmek için kullanılıyor.
import socket
import datetime
import pickle
import platform
import subprocess


class client_paket_yoneticisi:
    # def __init__(self,server_ip,server_port=127,client_ip=IP(dst='1.1.1.1').src):
    def __init__(self,server_ip,server_port=127):
        self.server_ip=server_ip
        self.server_port=server_port
        self.baglanti = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.baglanti_durumu = 0
    def baglanti_kur(self):
        try:
            print("{}:{} ADRESINE BAĞLANTI KURULUYOR".format(self.server_ip,self.server_port))
            self.baglanti.connect((self.server_ip,self.server_port))
            print("baglanti basarili")
        except socket.error as msg:
            print("Socket Hatası: %s" % msg)
            print("PROGRAMDAN ÇIKILIYOR")
            exit(-1)

    def baglanti_kes(self):
        self.baglanti.close()

    def paket_gonder_al(self,mesaj):
        t0,t3 = 0,0
        try:
            print("Paket Gönderiliyor.")
            t0 = datetime.datetime.now()#istek paketi iletiminin zaman damgasıdır
            self.baglanti.sendall(mesaj.encode())

            print("{} Paketi Gönderildi".format(mesaj))

        except socket.error as msg:
            print("Socket Hatası: %s" % msg)
            print("PROGRAMDAN ÇIKILIYOR")
            exit(-1)

        donut = self.baglanti.recv(1024)
        t3 = datetime.datetime.now()    #yanıt paketi alımına ilişkin zaman damgasıdır.

        return donut,t0,t3



class zaman_yoneticisi:
    def __init__(self,paket_yoneticisi=client_paket_yoneticisi("1.1.1.1",127),alinan_zaman=0,t0=0,t1=0,t2=0,t3=0):
        self.paket_yoneticisi=paket_yoneticisi
        self.alinan_zaman=alinan_zaman
        self.t0=t0
        self.t1=t1
        self.t2=t2
        self.t3=t3
        self.timezone="NONE"
        self.gecikme = 0     #round-trip delay
        self.time_offset=0   #zaman kayması

    def zaman_istegi(self):
        mesaj,self.t0,self.t3=self.paket_yoneticisi.paket_gonder_al("TIME_REQUEST")
        mesaj = self.mesaj_duzenle(mesaj)
        self.t1=mesaj["T1"]
        self.t2 = mesaj["T2"]
        self.timezone = mesaj["TIMEZONE"]
        self.alinan_zaman=mesaj["ZAMAN"]
        print("ZAMAN DİLİMİ = {} ".format(self.timezone))


    def mesaj_duzenle(self,mesaj):
        return pickle.loads(mesaj)

    def zaman_hesapla(self):
        print("Zaman Hesabı Yapılıyor.")
        #Saat senkronizasyon algoritması https://en.wikipedia.org/wiki/File:NTP-Algorithm.svg
        # print(self.t3,self.t2,self.t1,self.t0)
        # offset değeri de 2 saat arasındaki hız farkından ortaya çıkan bir değermiş
        # şu ana kadar seri üretilen saatlerin çoğu belli bir zaman süre sonra 1-2 saniye geride kalıyormuş.
        # bunun için reference clock olarak kullanılan sezyum saatlerinden alınan değere göre offset değeri belirlenip
        # bilgisayar saati offset değeri üzerinden hesaplama yapıyormuş.
        # fakat bu ödevde offset değerini uygulayamadım.
        # print(self.t0,self.t1,self.t2,self.t3)
        saniye = self.alinan_zaman / 1000.0
        time = datetime.datetime.fromtimestamp(saniye)
        print("GECİKMELİ ZAMAN = ",time)
        gecikme = (self.t3-self.t0) - (self.t2-self.t1)  #CLIENTIN İÇERİSİNDE GEÇEN ZAMAN - SERVER İÇERİSİNDE GEÇEN ZAMAN +SON PAKET ALIMINDAN SONRA GEÇEN ZAMAN
        offset  = (self.t1-self.t0 + self.t2-self.t3)/2
        print("------------------------------------------")
        print("Gecikme(paket dolaşımı)= "+str(gecikme)+" ms")
        print("Offset (zaman kayması)=  "+str(offset)+" ms")       ####
        print("------------------------------------------")
        time = gecikme+datetime.datetime.fromtimestamp(saniye)
        print("GECİKMESİZ ZAMAN = ",time)
        print("------------------------------------------")
        self.zaman_ayarla(time)
    def zaman_ayarla(self,zaman):
        if platform.system() == "Linux":
            newdate = subprocess.Popen(["sudo", "date", "-s", str((zaman))])
            newdate.communicate()
            print("Saat güncellendi")

        else:
            print("Kodun bu kısmı sadece linuxta çalışmaktadır, çıkılıyor.")
            exit(1)


if __name__ == "__main__":
    #########################################################
    client_py = client_paket_yoneticisi("192.168.0.105", 127)  #BURAYA SERVER İP Sİ GİRİLECEK.
    #########################################################
    client_py.baglanti_kur()
    zy = zaman_yoneticisi(paket_yoneticisi=client_py)
    zy.zaman_istegi()
    zy.zaman_hesapla()
    client_py.baglanti_kes()

else:
    print("IMPORT YAPMAYINIZ.")

