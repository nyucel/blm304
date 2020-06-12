#Gökçe Kuler 160401045

import socket
import os
import sys
def dosya_kaydet(veri):
    dosya = open("cekilendosya.txt","wb")
    dosya.write(veri)
    dosya.close()

soket= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      
udp_port = 42			        
ipadresi=input("lütfen ip adresi giriniz")
mesaj = "Baglanti kuruldu"
while True:
    try:
        soket.sendto(mesaj.encode(),(ipadresi,udp_port))
    except:
        print("bağlantı kurulamadı")
        sys.exit()
    serverdosya,addr = soket.recvfrom(1024) #Server'ın bulunduğu dizindeki dosya isimlerini çekiyor
    print("Server'da ki dosyalar:",serverdosya)

    dosya_ismi=input("Dosya gönermek için PUT dosyaismi dosya almak için ise GET dosyaismi komutunu kullanınız \n")
    dosya_tum=dosya_ismi.split()
    blocksize=4096
    dosya_metod=dosya_tum[0] #yapılacak işlemi tutar
    dosya_ad=dosya_tum[1]    #dosyanın ismini tutar

    if(dosya_metod == "PUT"):
        try:
            soket.sendto(dosya_metod.encode(),(ipadresi,udp_port)) #Yapılacak işlemin ne olduğunu sunucuya gönderir
        except:
            print("Dosya metodu gönderilemedi")
            sys.exit()
        if os.path.exists(dosya_ad):
                with open(dosya_ad,"rb") as f:
                    paket = f.read(blocksize)
                        
                    while paket != '':
                        try:
                            soket.sendto(paket,(ipadresi,udp_port))
                        except:
                            print("Dosya gönderilemedi")
                            sys.exit()
                        paket = f.read(blocksize)
                        break                            
        else:
            print("Bu dizinde bu isimde bir dosya yoktur lütfen istemci ve sunucuyu baştan başlatarak tekrar deneyiniz")
            sys.exit()
        
    if(dosya_metod == "GET"):
        try:
            soket.sendto(dosya_metod.encode(),(ipadresi,udp_port))  #Yapılacak işlemin ne olduğunu sunucuya gönderir
        except:
            print("Dosya metodu gönderilemedi")
            sys.exit()
        try:    
            soket.sendto(dosya_ismi.encode(),(ipadresi,udp_port))
        except:
            print("Dosya ismi gönderilemedi")
            sys.exit()
        try:
            data,addr = soket.recvfrom(1024)
        except:
            print("Dosya cekilemedi")
        dosya_kaydet(data)
        
   
   
