from scapy.all import *
import time
import pickle
import sys
import hashlib


server_ip = ""
server_port = 42
client_port = 84
parcalanma_boyut = 0
dinleyici = AsyncSniffer()
gelen_paketler=[]
debug=0             # debug 1 olursa printleri açıyorum.
dosya_bilgileri=[]
alinan_dosya={}







def baslangic():
    global server_ip                #server ip değişkenini değiştirebilmek için kullanılıyor.

    print("Dosya Transferi İstemcisine Hoşgeldiniz.")
    server_ip=input("Lütfen server ip adresini giriniz= ")
    dinleme_baslat()
    yoklama_mesaji()
    menu()




def dinleme_baslat():
    global dinleyici
    dinleyici=AsyncSniffer(prn=alinan_paket_islemi,filter="udp and src host "+str(server_ip)+" and port "+str(client_port)+"")
    dinleyici.start()
    print("dinleyici başladı")

def mesaj_gonder(mesaj):
    global server_port
    global client_port
    global server_ip
    a = IP(dst=server_ip) / UDP(dport=server_port,sport=client_port) / mesaj
    #a.show()
    send(a)


def yoklama_mesaji():
    mesaj_gonder("Kullanici tarafindan selam!")
    for i in range(10):                                            #10 kere bağlanmak denenir.

        if "Server tarafindan selam!".encode() in gelen_paketler:  #server tarafindan mesaj geldi mi ?
            print("FTP SUNUCUNA BAĞLANTI KURULDU.")
            temizlik()
            return 1

        mesaj_gonder("Kullanici tarafindan selam!")
        print("Bağlanılmaya çalışılıyor." + str(10 - i))
        time.sleep(1)                                               #çok hızlı olursa paket kaçırıyor.

    print("servere bağlanılamadı programdan çıkış yapılıyor")
    temizlik()
    exit(1)


def alinan_paket_islemi(packet):
    # print("Paket Alındı")
    #packet.show()
    gelen_paketler.append(packet.getlayer(Raw).load)


def temizlik():#gelen önceki paketleri temizliyoruz.
    f = open("logs_file","ab+")
    pickle.dump(gelen_paketler,f)
    f.close()
    gelen_paketler.clear()          #paketleri temizleyelim.



def dosya_listele():
    mesaj_gonder("LS")
    iletildi_mi_komut("LS")
def dosya_indir(dosya):
    global alinan_dosya
    mesaj_gonder("GET "+dosya)
    if(iletildi_mi_komut("GET")):
        while(len(alinan_dosya) != int(dosya_bilgileri[3])):
            for paket in gelen_paketler:
                alinan_paketcik = paket.decode().split(" ")
                if alinan_paketcik[0] == "FILESEND" and alinan_paketcik[1] not in alinan_dosya:             #ALINAN PAKETCIK = ["FILESEND PARCA NUMARASI HEX"]
                    alinan_dosya[int(alinan_paketcik[1])]=alinan_paketcik[2]
                    print("Parça Sayısı = "+str(dosya_bilgileri[3]) + "/"+str(len(alinan_dosya)))
                    mesaj_gonder("OKFILE! "+str(alinan_paketcik[1]))                                        #ALINDI DİYE GÖNDER
                if alinan_paketcik[0] == "FILESEND" and alinan_paketcik[1] in alinan_dosya:                 #ALINDI FAKAT HALEN YOLLANIYORSA
                    print("Aynı paket yollandı")
                    mesaj_gonder("OKFILE! " + str(alinan_paketcik[1]))
    print("Bitti")
    dosya_birlestir(dosya_bilgileri[0])
    if hash_olustur(dosya_bilgileri[0]).hexdigest() != dosya_bilgileri[1]:
        print("Dosya Transferinde Bir Hata Meydana Geldi.Hashler Uyuşmuyor!!!!")
        mesaj_gonder("FINISH_TRANSFER_ERROR")

    else:
        print("Aktarım hash değerleri uyuşuyor. Dosya transferi başarılı")
        mesaj_gonder("FINISH_TRANSFER_BASARILI")

def dosya_birlestir(tofile):
    global alinan_dosya
    output = open(tofile, 'wb')
    for i in range(1,len(alinan_dosya)+1):
        output.write(bytes.fromhex(alinan_dosya[i]))
    output.close()




def iletildi_mi_komut(komut):
    print("KOMUT KONTROL EDİLİYOR.")
    baslangic_zamani=time.time()
    x=1
    if komut == "LS":
        while x:
            for paket in gelen_paketler:
                test = paket.decode().split(" ")
                if test[0]=="LS_OK!":
                    print("**********DOSYALAR************")
                    print(test[1])            #dosyalar
                    print("**********/DOSYALAR************")
                    x=0
            if int(time.time()-baslangic_zamani) > 10 :  #10 sn bekler
                print("Bağlantı zaman aşımına uğradı")
                x=0
        temizlik()
        return 1
    if komut == "GET":
        while x:
            for paket in gelen_paketler:
                test = paket.decode().split(" ")
                if test[0]=="INF-01":
                    global dosya_bilgileri
                    dosya_bilgileri.append(test[1])
                    dosya_bilgileri.append(test[2])
                    dosya_bilgileri.append(test[3])
                    dosya_bilgileri.append(test[4])
                    print("**********DOSYA ADI************")
                    print(test[1])            #dosyalar
                    print("**********DOSYA HASH************")
                    print(test[2])
                    print("**********DOSYA BOYUT************")
                    print(test[3])
                    print("**********DOSYA TAHMİNİ PARÇA SAYISI************")
                    print(test[4])
                    x=0
            if int(time.time()-baslangic_zamani) > 10 :  #10 sn bekler
                print("Bağlantı zaman aşımına uğradı")
                x=0
        temizlik()
        return 1
    if komut == "SND":
        while x:
            for paket in gelen_paketler:
                test = paket.decode().split(" ")
                if test[0]=="SEND_HANDSHAKE_OK!":
                    x=0
            if int(time.time()-baslangic_zamani) > 10 :  #10 sn bekler
                print("Bağlantı zaman aşımına uğradı")
                x=0
        temizlik()
        return 1





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



def dosya_gonder(dosya):
    mesaj_gonder("SND")
    if(iletildi_mi_komut("SND")):
        print("test")







def menu():
    while 1:
        print("************ANA MENÜ**************")
        # time.sleep(1)
        print()

        choice = input("""
                    1: DOSYALARI LİSTELE
                    2: DOSYA AL
                    3: DOSYA GÖNDER
                    Q: ÇIKIŞ

                    Lütfen seçiminizi yapın: """)

        if choice == "1":
            dosya_listele()
        elif choice == "2":
            dosya_indir(input("Lütfen Dosya İsmini Giriniz"))
        elif choice == "3":
            dosya_gonder(input("Lütfen Dosya İsmini Giriniz"))
        elif choice == "Q" or choice == "q":
            exit(0)





if __name__ == "__main__":
    baslangic()

