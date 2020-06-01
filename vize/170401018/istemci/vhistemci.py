# Cemre UZUN - 170401018 

from scapy.all import*
import os
import time


os.chdir("dosyaIstemci")  # Bir dizinden başka dizine geçmek için kullandık. Yani vh-istemci Klasorundeki "dosyaIstemci" klasorune işlem yapmak için geçtik.

hedefAdrIP = input("Baglanti kurulacak sunucu IP: ")  # Bağlantı kurulacak Server'ın IP bilgisi alındı ve kaydedildi.

while(True):  #MENÜ
    print("\n______________ MENU ________________ \n1. Listeleme icin 1'e basiniz..\n2. PUT icin 2'e basınız..\n3. GET icin 3'e basiniz..\n\n00. Cikis yapmak icin 00'a basiniz..\n")
    islem = int(input("Hangi islemi yapmak istiyorsunuz giriniz :  "))
    # İşlemler tanımlandı. Kullanıcıya sunuldu. Kullanıcı istediği işlemi seçer ve bu secim "islem" e atanır.

    if(islem == 1):      # Listeleme işlemi seçildiğinde bu işlem başlatılır.

        print("\n")

        packetUdp = IP( dst = hedefAdrIP ) / UDP( sport = 35, dport = 42 ) / Raw( load = "1" )
        send(packetUdp)  # Kullanıcının seçtiği islemi Sunucuya gönderdik.
        print("\n")

        sncDosyasi = sniff( count = 1, filter = "udp port 35", iface = "lo" )  # sniff ile yakalandı.
        print("\n_____ SUNUCU ICINDEKI DOSYALAR _____\n")
        print( sncDosyasi[0].load.decode() ) #dosyalar listelendi.
        print( "\n" )

    elif( islem == 2 ):  # Put işlemi seçildiğinde bu işlem başlatılır.

        dosName = input( "\nPUT islemi yapacaginiz dosya adi : ")

        if( os.path.exists(dosName) == True ):  # Dosyayı İstemci klasöründeki dosyada bulduysak bu if e girdik.
            print("\n")

            packetUdp = IP( dst = hedefAdrIP ) / UDP( sport = 35, dport = 42 ) / Raw( load = "2" )
            send(packetUdp)  # Sunucuya bilgi gönderdik.
            time.sleep(1)


            packetUdp = IP( dst = hedefAdrIP ) / UDP( sport = 35, dport = 42 ) / Raw( load = dosName )
            send(packetUdp)  # Dosya adını Sunucuya gönderdik.

            dos= open(dosName ,"rb")
            bilgi = dos.read()  # Dosya içeriğini okuduk kaydettik.
            dos.close()

            time.sleep(1)

            packetUdp = IP( dst = hedefAdrIP) / UDP(sport = 35, dport = 42) / Raw(load = bilgi)
            send(packetUdp)  # Sunucuya içeriği-bilgiyi ilettik.

            print("\n+++Dosya, Put islemi ile Sunucuya iletildi.. BASARILI!!")

        else:  # Bu kısımda istemcide bulunmayan bir dosya ismi girildiyse put işlemi için tekrar bir dosya ismi istenir.

                print("\n---Dosya Istemcide bulunamadi.. BASARISIZ!!")
                packetUdp = IP( dst = hedefAdrIP) / UDP(sport = 35, dport = 42) / Raw(load = "5")
                send(packetUdp)  # Dosyanin mevcut olmamasi halinde bir kontrol değeri olan var_1 degerini gonderdik.
                time.sleep(1)
        print("\n\n")

    elif(islem == 3):  # Get işlemi seçildiğinde bu işlem başlatılır.

        print("\n")

        packetUdp = IP( dst = hedefAdrIP) / UDP(sport = 35, dport = 42) / Raw(load = "3")
        send(packetUdp)  # Sunucu ya yapılacak işlem bilgisini gönderdik.
        time.sleep(1)

        dosName = input ( "\nGET islemi yapacaginiz dosya adi : " )
        packetUdp = IP( dst = hedefAdrIP) / UDP(sport = 35, dport = 42) / Raw(load = dosName)
        send(packetUdp)  # Dosya adını Sunucuya gönderdik.

        controlFile = sniff( count = 1, filter = "udp port 35", iface = "lo" )
        var_1 = int(controlFile[0].load.decode())  # Dosyanin mevcut olmamasi halinde bir kontrol değeri olan var_1 degerini gonderdik.

        if(var_1 == 1):  # var_1 = 1 ise dosya var demektir.

            gData = sniff( count = 1, filter = "udp port 35", iface = "lo" ) # Dosya içeriğini yakaldık.
            bilgi = gData[0].load

            # Dosya içeriği kaydedildi.
            dosyaYeni = open(dosName ,"wb")
            dosyaYeni.write(bilgi)
            dosyaYeni.close()

            print("\n+++Dosya, Get islemi ile Istemciye kaydedildi.. BASARILI!!.")

        else:  # Get islemi yapilacak dosya Server'da mevcut degil ise...
            print("\nDosya bulunamadi. Istemciye yuklenmesini istediginiz dosya yuklenemedi")

        print("\n\n")

    elif(islem == 00 ):  # Programi sonlandirma durumu

        print("\n")

        packetUdp = IP( dst = hedefAdrIP ) / UDP( sport = 35, dport = 42 ) / Raw( load = "0" )
        send(packetUdp)

        time.sleep(1)

        print("\n*__ ISTEMCI KAPATILDI __\n")
        break;

    else:  # Menu dışında klavyeden basılan herhangi bir tuşa basılırsa

        print("\n+++Tekrar deneyiniz.\nMenude bulunan islemler disinda bir islem yapamazsiniz.\n\n")
