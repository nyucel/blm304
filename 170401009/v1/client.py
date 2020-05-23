from scapy.all import *
import time
import pickle
import sys


server_ip = ""
server_port = 42
client_port = 84
parcalanma_boyut = 0
dinleyici = AsyncSniffer()
gelen_paketler=[]
debug=0             # debug 1 olursa printleri açıyorum.








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
            print(3)
        elif choice == "3":
            print(2)
        elif choice == "Q" or choice == "q":
            exit(0)





if __name__ == "__main__":
    baslangic()

