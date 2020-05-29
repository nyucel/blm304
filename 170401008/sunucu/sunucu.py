# -*- coding: utf-8 -*-
#Arzu TEPE 170401008


#sunucu
import socket
import os #dosya islemleri iÃ§in eklendi
import time

#def listele():  #dosya listeleme iÅŸlemleri    
   # os.chdir("SunucuDosya") #bulunduÄŸumuz pathten SunucuDosya sÄ±na ulasmak iÃ§in
   # dosyalar = (os.listdir(os.getcwd()))  #SunucuDosya daki dosyalarÄ± listeledik 
   # return dosyalar
print(os.getcwd())
os.chdir("SunucuDosya")  #sunucudaki dosyalarÄ±n bulundugu yer
dosyalar = (os.listdir(os.getcwd()))  #istemcideki dosyalar
a = os.getcwd()
#soket olusturuldu dinlenmeye baÅŸlandÄ±
host = input("bir IP giriniz: ")
port = 42
buffer = 4096
while(True):
    while(True):
        
        sunucu = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #ilk deger adresleme seklini gosetiyor TCP ve UDP iÃ§in ipv4, ikinci deger iletisim tipi(udp)
        print("soket olustu")   
        sunucu.bind((host,port)) #soket port ve host ile iliÅŸkilendirildi
        #print(listele())
        
        print("bekleniyor...")
        data, adres = sunucu.recvfrom(1024) #BaÄŸlantÄ± bekliyor
        #print(addr,"BaÄŸlandÄ±\n") #BaÄŸlananÄ±n adresi
        #dosya = listele()
        sunucu.sendto(str(dosyalar).encode(),adres)   #dosyalarÄ± istemci tarafÄ±na gonderiyoruz
        komut = sunucu.recv(buffer).decode()
        kmt,istenen = komut.split(" ")
        if(kmt == "GET"):
            if(istenen in dosyalar):  #istenen dosya listenin icinde mi diye bakÄ±ldÄ±
                boyut=os.stat(istenen).st_size
                sunucu.sendto(str(boyut).encode(),adres)  #dosya boyutu gonderildi
                file = istenen.encode()
                
    
                f = open(file, "rb")  #istenen dosya hazÄ±rlandÄ±
                a = f.read(buffer)  #sÄ±nÄ±r kadar okuyuyoruz parca parca gondermek icin
                #print(file)
                sunucu.sendto(file,adres)  #ismi gonderildi
                sunucu.sendto(a,adres)
                
                while (a):                                           
                        if(sunucu.sendto(a, adres)):
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
                            
                f.close()  #dosyayÄ± kapattÄ±k
            else:  #degilse -1 gonderilecek
                a = -1
                sunucu.sendto(str(a).encode(),adres)
                print("istenen dosya bulunamadı!!!")
            mesaj = sunucu.recv(buffer).decode()
            print(mesaj)
            sunucu.close()
            
            break
            
        elif(kmt == "PUT"):
            a = os.getcwd()
            boyut = sunucu.recv(buffer).decode() #boyutu aldÄ±k
            print(boyut)
            isim = sunucu.recv(buffer).decode()
            print(isim)
            if(isim == "-1"): #gelen mesajda dosya yok
                print("istenen dosya yok!!")
                break;
            else:
                
                f = open(a+'/'+isim, 'wb') #dosya oluÅŸturduk.
                
                data = sunucu.recv(buffer)  #icerik kÄ±smÄ±nÄ± aldÄ±k
                try:                                                            
                    while(data):
                        f.write(data)                        
                        sunucu.settimeout(2)    #sunucudan veri biterse durcak                    
                        data = sunucu.recvfrom(buffer)[0]
                        sunucu.sendto('True'.encode(), adres)
                    #print(data)               
                except socket.timeout:
                    f.close()
                size=str(os.stat(a+"/"+isim).st_size)
                
                if(int(boyut) <= int(size)):
                    sunucu.sendto("dosya alindi".encode(), adres)
                else:
                    print("alinamadi!!")        
            sunucu.close()
            break
                
            
        
