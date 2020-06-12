#Beyza ÇOBAN
#170401012

import socket
import os
import time
import sys
from time import sleep
from datetime import datetime, timezone, timedelta


PORT= 142
UTC = -2
IP= input("Sunucu Ip Giriniz : ")
#local 10.0.2.15
print("Bağlanılacak IP: ", IP)



utc_bilgisi = open("utc.txt", "w")
utc_bilgisi.write(str(UTC))
utc_bilgisi.close()



def gecikme_suresi(istemci):
    gonderim_zamani = datetime.utcnow() + timedelta(hours=UTC)
    istemci.send(bytes(str(gonderim_zamani), encoding='utf-8'))
    print("\n Zaman kontrolü için gönderim yapıldı\n")

    test = istemci.recv(1024)
    alim_zamani = datetime.utcnow() + timedelta(hours=UTC)
    print("\n İstemci tarafından gönderilen mesajın alındığı zaman hesaplandı\n")

    gecikmesuresi = (alim_zamani - gonderim_zamani) / 2
    return gecikmesuresi


def main():
    with socket.socket() as sunucu:
        try:
            sunucu.bind((IP, PORT))
        except:
            print("\n BAŞARISIZ!! Sunucu oluşturulamadı\n")
            sys.exit()
        print("\n BAŞARILI!! Sunucu oluşturuldu\n")

        while True:
            sunucu.listen()
            istemci, istemciadres = sunucu.accept()
            print("\n İstemci bağlantısı başarılı\n")
            with istemci:
                while True:
                    baglanti = istemci.recv(1024)
                    if not baglanti:
                        break

                    gecikmesuresi = gecikme_suresi(istemci)
                    print("\ngecikme_süresi:\n", gecikmesuresi)

                    yeni_zaman = datetime.utcnow() + timedelta(hours = UTC) + gecikmesuresi  #gecikme süresi eklenmiş zaman gönderildi
                    istemci.send(bytes(str(yeni_zaman) , encoding='utf-8'))
                    
               
        sunucu.close()
        print("\nsunucu kapatıldı\n")

if __name__ =="__main__":
    main()
