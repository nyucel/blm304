# Cemre UZUN - 170401018

from scapy.all import*
import os
import time

lo_interface = input( "lo veya baska bir interface bilgisi giriniz : " )  # Interface bilgisi aldık.

os.chdir( "dosyaSunucu" )  # Bir dizinden başka dizine geçmek için kullandık. Yani vh-sunucu Klasorundeki "dosyaSunucu" klasorune işlem yapmak için geçtik.

while True:

    data1 = sniff( count = 1, filter = "udp port 42", iface = "lo_interface" )  # Gönderilen iface dinlenip 42 nolu portu gördüğünde  1 paketi yakaladık.

    islem = int(data1[0].load.decode())  # Bu kısımda İstemciden gelen seçimi "islem" parametresine kaydettik.

    hedefAdrIP = data1[0][IP].src  # Hedef olan İstemcinin IP adresini aldık ve kaydettik.

    if(islem == 1):          # Kullanıcı LİSTELEME işlemi yapacaktır.
                             # Listeleme işlemi seçilme durumunda kullanıcı istemciden 1 i seçmiştir.
        print("\n")
        time.sleep(1)                 # Uyutma işlemi

        packetUdp = IP( dst = hedefAdrIP ) / UDP( sport = 42, dport = 35 ) / Raw( load = "\n".join( os.listdir() ) ) # Gönderilecek UDP paketi
        send(packetUdp)
        # İstemciye gönderilmek üzere sunucu klasörünün içindeki "dosyaSunucu" klasöründeki dosyalar liste halinde başarıyla İstemciye gönderdik.

        print( "\n+++Sunucuda bulunan dosyalar listelendi.. BASARALI!!\n\n" )

    elif(islem == 2):  # Kullanıcı PUT işlemi yapacaktır.
                        # Put işlemi seçilme durumunda kullanıcı istemciden 2 i seçmiştir.
        print("\n")
        data1 = sniff(count = 1, filter = "udp port 42", iface = "lo_interface")  # Gönderilen iface dinlenip 42 nolu portu gördüğünde  1 paketi-dosyayı yakaladık.
        dosName = data1[0].load.decode()  # Dosyanın adını dosName de tuttuk.

        data2 = sniff(count = 1, filter = "udp port 42", iface = "lo_interface") # Gönderilen iface dinlenip 42 nolu portu gördüğünde  1 paketi-dosyayı yakaladık.
        dosyaic = data2[0].load                                                  # Dosyanın içeriğini dosyaic de tuttuk.

        # Kullanıcı tam olarak seçtiği doyayı vh-sunucu klasörü içerisindeki "dosyaSunucu" klasörüne eklemek istemişti.
        newDos = open( dosName ,"wb" )  # Dosyayı ekledik.
        newDos.write(dosyaic)
        newDos.close()

        print( "\n+++Put islemi ile dosya eklendi.. BASARILI!!\n" )

    elif(islem == 3):  # Kullanıcı GET işlemi yapacaktır.

        print("\n")

        data1 = sniff(count = 1, filter = "udp port 42", iface = "lo_interface")
        dosName = data1[0].load  # Dosyayı kaydettik.

        if os.path.exists(dosName) == True:  # Kulanıcının girdisi olan dosya Sunucu dosyasında var mı onun kontrolü yapılır.
            time.sleep(1)
            packetUdp = IP(dst = hedefAdrIP) / UDP(sport = 42, dport = 35) / Raw(load = "1")
            send(packetUdp)             # Dosya var ise istemciye 1 değeri gönderdik.

            getDos = open(dosName ,"rb")  # Dosyayı okunduk kaydettik.
            dosyaic = getDos .read()
            getDos.close() #dosya kapatıldı.

            time.sleep(1)

            packetUdp = IP( dst = hedefAdrIP) / UDP(sport = 42, dport = 35) / Raw(load = dosyaic)
            send(packetUdp)  # Dosya içeriğini İstemciye gönderdik.

            print("\n** GET islemi basariyla gerceklesti..\n")

        else:

            time.sleep(1)
            packetUdp = IP(dst = hedefAdrIP) / UDP(sport = 42, dport = 35) / Raw(load = "0")
            send(packetUdp)
            print("\n--Istenilen dosya bulunamadi.. BASARISIZ!!\n")

    elif(islem == 00):
        print("\n__ SUNUCU KAPATILDI __\n")
        break;
