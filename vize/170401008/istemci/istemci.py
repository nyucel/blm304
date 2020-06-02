# -*- coding: utf-8 -*-
#170401008 Arzu TEPE

#istemci
import socket
import os
import time

host = input("bir IP giriniz: ")
port = 42
buffer = 4096 #boyutu sınırlamak için
while(True):
    sunucu = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    sunucu.sendto("baglandı ".encode(), (host, port))  #sunucuya mesaj gonderildi
    #sunucu.bind((host,port))
    os.chdir("IstemciDosya")  #istemcideki dosyaların bulundugu yer
    dosyalar = (os.listdir(os.getcwd()))  #istemcideki dosyalar
    a = os.getcwd()
    dosya = sunucu.recv(buffer)  #server dosyaları
    
    print("Serverdaki Dosyalar..:",dosya.decode())  #servardaki dosyaları yazdırdık
    print("Islemlerden birini seciniz: ")
    girilen = input("Dosya gondermek icin : Get dosya_adı.uzantısı/ yüklemek için PUT dosya_adi.uzantisi: ")
    sunucu.sendto(girilen.encode(),(host,port))  #istenen ve komutu sunucuya gonderdik
    komut,istenen = girilen.split(" ") #get/put komutunu ve dosya adını ayırdık
    
        
    if(girilen.find('GET') == 0):
        boyut = sunucu.recv(buffer).decode() #boyutu aldık
        
        isim = sunucu.recv(buffer).decode()
        
        if(isim == "-1"): #gelen mesajda dosya yok
            print("istenen dosya yok!!")
            break;
        else:            
            f = open(a+'/'+isim, 'wb') #dosya oluşturduk.            
            data = sunucu.recv(buffer)  #icerik kısmını aldık
            try:                                                            
                while(data):
                    f.write(data)                        
                    sunucu.settimeout(2)    #sunucudan veri biterse durcak                    
                    data = sunucu.recvfrom(buffer)[0]                    
                    sunucu.sendto('True'.encode(), (host, port))#verinin alindigi bilgisini gonderiyoruz               
            except socket.timeout:
                f.close()
            size=str(os.stat(a+"/"+isim).st_size)
            
            if(int(boyut) <= int(size)):
                sunucu.sendto("dosya alındı ".encode(), (host, port))  
            else:
                print("alınamadı!!")        
        sunucu.close()
        break
            
    elif(girilen.find('PUT') == 0):
        if(istenen in dosyalar):  #istenen dosya listenin icinde mi diye bakıldı
            boyut=os.stat(istenen).st_size
            sunucu.sendto(str(boyut).encode(),(host,port))  #dosya boyutu gonderildi
            file = istenen.encode()
            f = open(file, "rb")  #istenen dosya hazırlandı
            a = f.read(buffer)  #sınır kadar okuyuyoruz parca parca gondermek icin
            
            sunucu.sendto(file,(host,port))  #ismi gonderildi
            sunucu.sendto(a,(host,port))
            
            while (a):                                           
                    if(sunucu.sendto(a, (host,port))):
                        #print ("gonderiliyor ...")
                        a = f.read(buffer) 
                        time.sleep(0.0001)

                        try:     #dosyanin iletildi bilgisini bekledik
                            sunucu.settimeout(3)
                            kontrol = sunucu.recvfrom(buffer)[0].decode()
                            
                            #if(kontrol == 'True'):   #iletilme durumunu yazdirdik
                                #print('dosya gonderildi')
                        except socket.timeout:
                            break
                            print('dosya gonderilemedi')
            
            f.close()  #dosyayı kapattık
        else:  #degilse -1 gonderilecek
            a = -1
            sunucu.sendto(str(a).encode(),(host,port))
            print("istenen dosya bulunamadı!!!")

        mesaj = sunucu.recv(buffer).decode()
        print(mesaj)
        sunucu.close()
        break
    
    
   
