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

        if self.komut == "HANDSHAKE":
            dinleyici = AsyncSniffer(prn=self.donut_bekle,
                                     filter="udp and src host " + str(self.dIp) + " and src port " + str(
                                         self.dPort) + "")

            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(
                load="FTP_CLIENT_HANDSHAKE")
            dinleyici.start()
            while self.durum:  # paket görevini tamamlayana kadar.
                send(a, verbose=False)
                time.sleep(0.001)  # SLEEP VERİLMEZSE PAKET SİSTEMİNDE ARIZA OLUŞUYOR.
            dinleyici.stop()
###################################################################################
        if self.komut == "LS":
            dinleyici = AsyncSniffer(prn=self.donut_bekle,
                                     filter="udp and src host " + str(self.dIp) + " and src port " + str(
                                         self.dPort) + "")

            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(load="LS")
            dinleyici.start()
            while self.durum:  # paket görevini tamamlayana kadar.
                send(a, verbose=False)
                time.sleep(1)  # SLEEP VERİLMEZSE PAKET SİSTEMİNDE ARIZA OLUŞUYOR.
            dinleyici.stop()
####################################################################################
        if self.komut == "GET":
            dinleyici = AsyncSniffer(prn=self.donut_bekle,
                                     filter="udp and src host " + str(self.dIp) + " and src port " + str(
                                         self.dPort) + "")

            temp_mesaj = "GET " + self.data
            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(load=temp_mesaj)
            dinleyici.start()
            while self.durum:  # paket görevini tamamlayana kadar.
                send(a, verbose=False)
                time.sleep(1)  # SLEEP VERİLMEZSE PAKET SİSTEMİNDE ARIZA OLUŞUYOR.
            dinleyici.stop()
        if self.komut == "GET_FILE":
            dinleyici = AsyncSniffer(prn=self.donut_bekle,
                                     filter="udp and src host " + str(self.dIp) + " and src port " + str(
                                         self.dPort) + "")
            dinleyici.start()
            while self.durum:  # paket görevini tamamlayana kadar.
                time.sleep(0.001)  # SLEEP VERİLMEZSE PAKET SİSTEMİNDE ARIZA OLUŞUYOR.
            dinleyici.stop()
        if self.komut == "GET_FILE_END":

            temp_mesaj = "GET_FINISH_BASARILI"
            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(load=temp_mesaj)
            for i in range(20):  # kabafix
                send(a, verbose=False)
            self.data.clear()
        # if self.komut == "PUT":
#############################################################################
        if self.komut == "PUT_INFO":
            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(load=self.data)
            send(a)
            return 1

        if self.komut == "PUT_FILEPART":

            dinleyici = AsyncSniffer(prn=self.donut_bekle,
                                     filter="udp and src host " + str(self.dIp) + " and src port " + str(
                                         self.dPort) + "")

            a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(load=self.data)

            dinleyici.start()
            while self.durum:  # paket görevini tamamlayana kadar.
                send(a)
                time.sleep(0.001)  # SLEEP VERİLMEZSE PAKET SİSTEMİNDE ARIZA OLUŞUYOR.
            dinleyici.stop()
            return 1

    def donut_bekle(self, paket):
        if self.komut == "HANDSHAKE":
            temp_paket = self.raw_data_cozucu(paket)
            if "FTP_SERVER_HANDSHAKE_OK" in temp_paket:
                print("SERVERE BAĞLANILDI")
                self.durum = 0  # peket görevini tamamladı
                # burada dosyaları return edebilir.Ftp kontrol amaçlı

        if self.komut == "LS":
            temp_paket = self.raw_data_cozucu(paket)
            if "LS_OK" in temp_paket:
                temp_paket.remove("LS_OK")
                print("SERVER DOSYALARI")
                print("----------------")
                for x in temp_paket:
                    print(x)
                self.durum = 0  # peket görevini tamamladı
                # burada dosyaları return edebilir.Ftp kontrol amaçlı

        if self.komut == "GET":
            temp_paket = self.raw_data_cozucu(paket)
            if "GET_ERROR" in temp_paket:
                # print("DOSYA BULUNAMADI")
                self.data = -1  # DOSYA BULUNAMADI FLAG
                self.durum = 0  # görev tamamlanamadı
                # burada dosyaları return edebilir.Ftp kontrol amaçlı
            elif "GET_INFO" in temp_paket:
                # print(temp_paket)
                self.data = temp_paket
                self.durum = 0  # peket görevini tamamladı
                # burada dosyaları return edebilir.Ftp kontrol amaçlı
            # elif "GET_FILEPART" in temp_paket:
            # print(temp_paket)

        if self.komut == "GET_FILE":
            temp_paket = self.raw_data_cozucu(paket)
            if "GET_FILEPART" in temp_paket:
                self.data[int(temp_paket[1])] = temp_paket[2]  # İNT FİX
                temp_mesaj = "GET_FILEPART_OK " + str(temp_paket[1])
                a = IP(dst=self.dIp, src=self.sIp) / UDP(dport=self.dPort, sport=self.sPort) / Raw(load=temp_mesaj)
                send(a, verbose=False)
                self.durum = 0  # görev tamamlanamadı
                # burada dosyaları return edebilir.Ftp kontrol amaçlı

        if self.komut == "PUT_FILEPART":
            temp_paket = self.raw_data_cozucu(paket)
            if "PUT_FILEPART_OK" in temp_paket:
                if self.data.split(" ")[1] in temp_paket:  # GELEN PARÇA NUMARASI GİDENE EŞİT Mİ ?
                    print("BAŞARILI PARÇA", self.data.split(" ")[1])
                    self.durum = 0  # peket görevini tamamladı
                # burada dosyaları return edebilir.Ftp kontrol amaçlı


    def raw_data_cozucu(self, paket):
        return paket.getlayer(Raw).load.decode().split(" ")


class client:

    def __init__(self, dinleme_port=84, client_ip=str(IP(dst="1.1.1.1").getlayer(IP).src), server_port=42):
        self.server_port = server_port
        self.dinleme_port = dinleme_port
        self.client_ip = client_ip  # LOCAL IP ADRESIMIZI OGRENMEMIZI SAGLIYOR
        # USTTEKI SATIRDA BIR PROBLEM OLURSA MANUEL OLARAK GIRILEBILIR.

    def menu(self):
        print("FTP İSTEMCİSİNE HOŞGELDİN")
        print("IP -> ", self.client_ip, ":", self.dinleme_port)
        print("-------------------------")
        server_ip = input("Lutfen Server Ip Adresini Giriniz")
        test = paket(dport=self.server_port, sport=self.dinleme_port, dIp=server_ip, sIp=self.client_ip,
                     komut="HANDSHAKE")
        test.calistir()
        test2 = paket(dport=self.server_port, sport=self.dinleme_port, dIp=self.client_ip, sIp=self.client_ip,
                      komut="LS")
        test2.calistir()

        while 1:

            print("İŞLEM NUMARASINI YAZ")
            print("--------------------")
            print("1 | LS")
            print("2 | DOSYA AL")
            print("3 | DOSYA GÖNDER")
            print("4 | ÇIKIŞ")
            print("--------------------")
            secenek = input("İŞLEM NUMARASI = ")

            if secenek == "1":
                test2 = paket(dport=self.server_port, sport=self.dinleme_port, dIp=self.client_ip, sIp=self.client_ip,
                              komut="LS")
                test2.calistir()
            elif secenek == "2":
                dosya_secenek = input("Dosya ismi = ")
                test3 = paket(dport=self.server_port, sport=self.dinleme_port, dIp=self.client_ip, sIp=self.client_ip,
                              komut="GET",
                              data=dosya_secenek)
                test3.calistir()
                if test3.data == -1:  # dosya bulunamadı
                    print("DOSYA BULUNAMADI")
                else:
                    print("DOSYA İSMİ -> ", test3.data[1])
                    print("DOSYA BOYUTU ->", test3.data[3])
                    print("DOSYA PARCA SAYISI ->", test3.data[4])
                    print("DOSYA CHUNK SIZE ->", test3.data[5])
                    print("DOSYA HASH(B2SUM) ->", test3.data[2])

                    dosya_temp = dosya(dosya_adi=test3.data[1], dosya_boyut=test3.data[3],
                                       dosya_chunk_boyut=test3.data[5], hash=test3.data[2],
                                       parca_sayisi=test3.data[4])

                    while int(dosya_temp.parca_sayisi) != len(dosya_temp.cache):
                        test3 = paket(dport=self.server_port, sport=self.dinleme_port, dIp=self.client_ip, sIp=self.client_ip,
                                      komut="GET_FILE")
                        test3.calistir()
                        dosya_temp.cache.update(test3.data)
                        temp_len = len(dosya_temp.cache)
                        print(dosya_temp.parca_sayisi,"/",str(temp_len))
                    test3 = paket(dport=self.server_port, sport=self.dinleme_port, dIp=self.client_ip, sIp=self.client_ip,
                                  komut="GET_FILE_END")
                    test3.calistir()
                    print("DOSYA ALINDI")
                    print("DOSYA BİRLEŞTİRİLİYOR")
                    # print(dosya_temp.cache)
                    dosya_temp.birlestir()  # RAME CACHE OLARAK ALINMIŞ PARÇALARI BİRLEŞTİRİR.
                    # DOSYAYA YAZAR
                    # HASHLERİ DE KONTROL EDİYOR.
                    print("İŞLEM TAMAMLANDI")

                    # self, dosya_adi, dosya_boyut = 0, parca_sayisi = 0, hash = 0, dosya_chunk_boyut = 0

            elif secenek == "3":
                dosya_yolu = input("Dosya ismi = ")
                if (os.path.exists(dosya_yolu)):
                    temp_dosya = dosya(dosya_adi=dosya_yolu)
                    temp_dosya.bilgi_hesapla()
                    temp_data = "PUT_INFO" + ' ' + str(temp_dosya.dosya_adi) + ' ' + str(temp_dosya.hash) + ' ' + str(
                        temp_dosya.boyut) + ' ' + str(temp_dosya.parca_sayisi) + ' ' + str(temp_dosya.chunk_boyut)
                    test3 = paket(dport=self.server_port, sport=self.dinleme_port, dIp=server_ip, sIp=self.client_ip,
                                  komut="PUT_INFO",
                                  data=temp_data)
                    for i in range(10):
                        test3.calistir()
                    temp_dosya.cache_al()
                    while 1:  # Dosya Aktarılana kadar
                        if len(temp_dosya.cache) > 0:
                            key_copy = tuple(temp_dosya.cache.keys())  # changed size during iteration error FİX

                            for y in key_copy:  # changed size during iteration error FİX
                                # eğer bu işlemi yapmayıp, x in temp_dosya.cache yaparsam sıkıntı oluyor
                                temp_data = "PUT_FILEPART" + ' ' + str(y) + ' ' + temp_dosya.cache[y]
                                temp_paket2 = paket(dport=self.server_port, sport=self.dinleme_port, dIp=server_ip,
                                                    sIp=self.client_ip,
                                                    komut="PUT_FILEPART",
                                                    data=temp_data)
                                temp_paket2.calistir()
                                del temp_dosya.cache[y]
                        else:
                            break



                else:
                    print("DOSYA BULUNAMADI.")

            elif secenek == "4":
                exit(0)
            else:
                print("Lütfen Düzgün Bir İşlem Numarası Girin")


cli = client()
cli.menu()

# test2 = paket(dport=self.server_port, sport=self.dinleme_port, dIp=self.client_ip, sIp=self.client_ip, komut="LS")
# test3 = paket(dport=self.server_port, sport=self.dinleme_port, dIp=self.client_ip, sIp=self.client_ip, komut="GET",data="test.png")


# test2.calistir()
# test3.calistir()
