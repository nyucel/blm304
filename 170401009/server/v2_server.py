#ATAKAN TÜRKAY 170401009

from scapy.all import *
import time
import sys
import hashlib
from pathlib import Path
from math import ceil  # parca sayisi hesaplanirken 5.1 de olsa 6 parca oluyor.O yüzden yukarı yuvarlamak gerekiyor.


class dosya:

    def __init__(self, dosya_adi, dosya_boyut=0, parca_sayisi=0, hash=0, dosya_chunk_boyut=512):
        self.dosya_adi = dosya_adi
        self.boyut = dosya_boyut
        self.chunk_boyut = dosya_chunk_boyut
        self.parca_sayisi = parca_sayisi
        self.hash = hash
        self.cache = {}

    def bilgi_hesapla(self):
        self.boyut = Path(self.dosya_adi).stat().st_size
        self.parca_sayisi = ceil(self.boyut / self.chunk_boyut)
        self.hash_hesapla()

    def birlestir(self):
        output = open(self.dosya_adi, 'wb')
        for i in range(1, len(self.cache) + 1):
            output.write(bytes.fromhex(self.cache[i]))
        output.close()
        if (self.hash != self.hash_return()):
            print("Dosya hashleri uyuşmuyor.")
            return -1

    def cache_al(self):  # dosyaları parçalanma boyutuna kadar chunklar halinde rame bir sözlük şeklinde depoluyor.
        partnum = 0
        input = open(self.dosya_adi, 'rb')  # use binary mode on Windows
        while 1:  # eof=empty string from read
            chunk = input.read(self.chunk_boyut)  # get next part <= chunksize
            if not chunk: break
            partnum = partnum + 1
            filename = partnum
            self.cache[filename] = chunk.hex()  # DOSYANUMARASI BOŞLUK CHUNK un hex hali (byte normalde)
        input.close()

    def hash_hesapla(self):
        file_hash = hashlib.blake2b()  # b2sum
        with open(self.dosya_adi, "rb") as f:
            while 1:
                chunk = f.read(8192)
                if not chunk:
                    break
                file_hash.update(chunk)
                f.read(8192)
            f.close()
        self.hash = file_hash.hexdigest()

    def hash_return(self):
        file_hash = hashlib.blake2b()  # b2sum
        with open(self.dosya_adi, "rb") as f:
            while 1:
                chunk = f.read(8192)
                if not chunk:
                    break
                file_hash.update(chunk)
                f.read(8192)
            f.close()
        return file_hash.hexdigest()


class paket:

    def __init__(self, dport=0, sport=0, dIp="", sIp="", data={}, komut=""):
        self.dPort = dport
        self.sPort = sport
        self.dIp = dIp
        self.sIp = sIp
        self.data = data
        self.komut = komut
        self.dinleyici = AsyncSniffer()
        self.durum = 1  # durum 1 iken paket görevini tamamlamamıştır.
        # durum 0 iken paket görevini tamamlamıştır.

    def calistir(self):
        if self.komut == "LS":
            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(load=self.data)
            send(a)
            return 1
        if self.komut == "HANDSHAKE":
            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(
                load="FTP_SERVER_HANDSHAKE_OK")
            send(a)
            return 1

        if self.komut == "GET_INFO":
            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(load=self.data)
            send(a)
            return 1

        if self.komut == "GET_FILEPART":

            dinleyici = AsyncSniffer(prn=self.donut_bekle,
                                     filter="udp and src host " + str(self.dIp) + " and src port " + str(
                                         self.dPort) + "")

            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(load=self.data)

            dinleyici.start()
            while self.durum:  # paket görevini tamamlayana kadar.
                send(a)
                time.sleep(0.00001)  # SLEEP VERİLMEZSE PAKET SİSTEMİNDE ARIZA OLUŞUYOR.
            dinleyici.stop()
            return 1

        if self.komut == "GET_ERROR":
            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(
                load="GET_ERROR")
            send(a)
            return 1

        if self.komut == "PUT_FILE":
            dinleyici = AsyncSniffer(prn=self.donut_bekle,
                                     filter="udp and src host " + str(self.dIp) + " and src port " + str(
                                         self.dPort) + "")
            dinleyici.start()
            while self.durum:  # paket görevini tamamlayana kadar.
                time.sleep(0.00001)  # SLEEP VERİLMEZSE PAKET SİSTEMİNDE ARIZA OLUŞUYOR.
            dinleyici.stop()


    def donut_bekle(self, paket):
        if self.komut == "GET_FILEPART":
            temp_paket = self.raw_data_cozucu(paket)
            if "GET_FILEPART_OK" in temp_paket:
                if self.data.split(" ")[1] in temp_paket:  # GELEN PARÇA NUMARASI GİDENE EŞİT Mİ ?
                    print("BAŞARILI PARÇA", self.data.split(" ")[1])
                    self.durum = 0  # peket görevini tamamladı
                # burada dosyaları return edebilir.Ftp kontrol amaçlı

        if self.komut == "PUT_FILE":
            temp_paket = self.raw_data_cozucu(paket)
            if "PUT_FILEPART" in temp_paket:
                self.data[int(temp_paket[1])] = temp_paket[2]  # İNT FİX
                temp_mesaj = "PUT_FILEPART_OK " + str(temp_paket[1])
                a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(load=temp_mesaj)
                send(a, verbose=False)
                self.durum = 0  # görev tamamlanamadı
                # burada dosyaları return edebilir.Ftp kontrol amaçlı

    def raw_data_cozucu(self, paket):
        return paket.getlayer(Raw).load.decode().split(" ")


class server:
    def __init__(self):
        self.dinleme_port = 42
        self.server_ip = str(IP(dst="1.1.1.1").getlayer(IP).src)  # LOCAL IP ADRESIMIZI OGRENMEMIZI SAGLIYOR
        # USTTEKI SATIRDA BIR PROBLEM OLURSA MANUEL OLARAK GIRILEBILIR.
        self.bagli_cihazlar = []
        self.dinleyici = AsyncSniffer().start()  # ASENKRON DINLEYİCİ BAŞLIYOR
        self.getdosya={}
        self.dinleme()

        while 1:
            print(self.server_ip, ":", self.dinleme_port, " Dinliyor...")
            print(len(self.bagli_cihazlar))
            time.sleep(1)

    def dinleme(self):
        self.dinleyici = AsyncSniffer(prn=self.donut_bekle,
                                 filter="udp and dst port " + str(self.dinleme_port) + "")
        self.dinleyici.start()

    def reset(self):
        self.dinleyici.stop()
        self.dinleme()

    def donut_bekle(self, packet):
        client_ip, client_port, data = packet.getlayer(IP).dst, packet.getlayer(IP).sport, self.raw_data_cozucu(packet)
        print("42 PORTU PAKET YAKALADI.")
        # print(packet)

        """
        FTP SERVER HANDSHAKE
        """
        if "FTP_CLIENT_HANDSHAKE" in data:
            print("HANDSHAKE YAKALANDI")
            test = paket(dport=client_port, sport=self.dinleme_port, dIp=client_ip, sIp=self.server_ip,
                         komut="HANDSHAKE")
            test.calistir()
            if client_ip not in self.bagli_cihazlar:
                self.bagli_cihazlar.append(client_ip)# clientimizi whitelist e alıyoruz.


        """
        LS KOMUTU GELDİĞİ ZAMAN EĞER CLİENT WHITELISTTEYSE
        KOMUTU UYGULAR
        """
        if ("LS" in data) and (client_ip in self.bagli_cihazlar):  # ip adresi whitelist te olmak zorunda
            print("LS YAKALANDI")
            test = paket(dport=client_port, sport=self.dinleme_port, dIp=client_ip, sIp=self.server_ip, komut="LS",
                         data="LS_OK " + ' '.join(os.listdir()))
            test.calistir()

        """
        GET KOMUTU GELDİĞİ ZAMAN EĞER CLİENT WHITELISTTEYSE
        KOMUTU UYGULAR DOSYA BİLGİLERİNİ GÖNDERİR VE DOSYA AKTARIMI İÇİN BİR BAŞKA KOMUTU ÇAĞIRIR.
        """

        if ("GET" in data) and (client_ip in self.bagli_cihazlar):  # ip adresi whitelist te olmak zorunda
            print(self.bagli_cihazlar)
            print("IP -> ", client_ip, ":", client_port, "GET -> ", data[1])
            if (os.path.exists(data[1])):
                temp_dosya = dosya(dosya_adi=data[1])
                temp_dosya.bilgi_hesapla()
                temp_data = "GET_INFO" + ' ' + str(temp_dosya.dosya_adi) + ' ' + str(temp_dosya.hash) + ' ' + str(
                    temp_dosya.boyut) + ' ' + str(temp_dosya.parca_sayisi) + ' ' + str(temp_dosya.chunk_boyut)
                temp_paket = paket(dport=client_port, sport=self.dinleme_port, dIp=client_ip, sIp=self.server_ip,
                                   komut="GET_INFO",
                                   data=(temp_data))
                for i in range(10):  # 10 kere  yolluyorum dosya infosunu
                    temp_paket.calistir()
                temp_dosya.cache_al()
                while 1:  # Dosya Aktarılana kadar
                    if len(temp_dosya.cache) > 0:
                        key_copy = tuple(temp_dosya.cache.keys())   # changed size during iteration error FİX

                        for y in key_copy:  # changed size during iteration error FİX
                            # eğer bu işlemi yapmayıp, x in temp_dosya.cache yaparsam sıkıntı oluyor
                            temp_data = "GET_FILEPART" + ' ' + str(y) + ' ' + temp_dosya.cache[y]
                            temp_paket2 = paket(dport=client_port, sport=self.dinleme_port, dIp=client_ip,
                                                sIp=self.server_ip,
                                                komut="GET_FILEPART",
                                                data=temp_data)
                            temp_paket2.calistir()
                            print("gönderilen ",str(y))
                            del temp_dosya.cache[y]
                    else:
                        break


            else:
                temp_paket = paket(dport=client_port, sport=self.dinleme_port, dIp=client_ip, sIp=self.server_ip,
                                   komut="GET_ERROR")
                temp_paket.calistir()

            if ("GET_FINISH_BASARILI" in data) and (client_ip in self.bagli_cihazlar):
                print("Aktarım Başarılı")
                exit(1)
            # test = paket(dport=84, sport=42, dIp=client_ip, sIp="192.168.1.101", komut="LS", data = "LS_OK "+' '.join(os.listdir()))
            # test.calistir()

        if ("PUT_INFO" in data) and (client_ip in self.bagli_cihazlar):  # ip adresi whitelist te olmak zorunda

            print("DOSYA İSMİ -> ",data[1])
            print("DOSYA BOYUTU ->", data[3])
            print("DOSYA PARCA SAYISI ->", data[4])
            print("DOSYA CHUNK SIZE ->", data[5])
            print("DOSYA HASH(B2SUM) ->", data[2])

            dosya_temp = dosya(dosya_adi=data[1], dosya_boyut=data[3],
                               dosya_chunk_boyut=data[5], hash=data[2],
                               parca_sayisi=data[4])
            while int(dosya_temp.parca_sayisi) != len(dosya_temp.cache):
                test3 = paket(dport=client_port, sport=self.dinleme_port, dIp=client_ip, sIp=self.server_ip,
                              komut="PUT_FILE")
                test3.calistir()
                dosya_temp.cache.update(test3.data)
                print(dosya_temp.parca_sayisi, end=" ")
                print(len(dosya_temp.cache), end=" ")

            dosya_temp.birlestir()
            print("İŞLEM TAMAMLANDI")

    

    def raw_data_cozucu(self, paket):
        return paket.getlayer(Raw).load.decode().split(" ")


main_server = server()
