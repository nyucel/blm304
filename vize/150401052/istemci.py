#Erdin Alhas 150401052

import os
import sys
import time
from socket import *
from os import system, name                                                           
def dosyaYukle(dosyaIsmi, dosyaIcerigi):                                                       
    if(os.path.exists(dosyaIsmi) == True):                                                   
        print('\nIstemci icerisinde "', dosyaIsmi, '" isimli dosya mevcut kopya olusturuluyor \n')
        yeniIsim = dosyaIsmi[:-4] + "(kopya)" + ".txt"
        yeniDosya = open(yeniIsim, "wb")
        yeniDosya.write(dosyaIcerigi)
        yeniDosya.close()
        sys.exit()                                                                           
    else:                                                                                   
        yeniDosya = open(dosyaIsmi, "wb")
        yeniDosya.write(dosyaIcerigi)
        yeniDosya.close()
        sys.exit()        
os.chdir("istemci dosyaları")                                                                                                                                 
ip = input("\nSunucu IP giriniz: ")
port = 42
i_soket = socket(AF_INET, SOCK_DGRAM)
i_soket.sendto(bytes("kontrol", encoding='utf-8'), (ip, port)) 
try:
    kontrol = i_soket.recvfrom(4096)                                                  
    print("\n ", kontrol[0].decode("utf-8"), "\n")
except:                                                                                     
    print("\nSunucu hazir değil. İlk olarak sunucuyu hazir ediniz.\n")
    sys.exit()
print("\n 1-Listele\n2-PUT\n3-GET\n4-Sonlandir\n")
tercih = int(input("Secim yapiniz: "))
if(tercih == 1):
    i_soket.sendto(bytes("listeleme yap", encoding='utf-8'), (ip,port))
    sunucuDosyalar = i_soket.recvfrom(4096)
    print("Sunucu Dosyalari Listesi: \n")
    print(sunucuDosyalar[0].decode("utf-8"))
    sys.exit()
elif(tercih == 2):
    dosyaIsmi = input("\nPUT islemi icin dosya adini giriniz: ")
    i_soket.sendto(bytes("put yap", encoding='utf-8'), (ip, port))            
    if(os.path.exists(dosyaIsmi) == True):                                                    
        i_soket.sendto(bytes("mevcut", encoding='utf-8'), (ip, port))    
        i_soket.sendto(bytes(dosyaIsmi, encoding='utf-8'), (ip, port))
        dosya = open(dosyaIsmi, "rb")                                                         
        dosyaIcerik = dosya.read()
        dosya.close()
        i_soket.sendto(dosyaIcerik, (ip, port))
        kontrol = i_soket.recvfrom(4096)
        if(kontrol[0].decode("utf-8") == "tamam"):                                          
            print("\nDosya basariyla sunucuya yuklenmistir...")
        else:                                                                               
            print('\nSunucu icerisinde "', dosyaIsmi, '" adinda bir dosya mevcut')
            print("\nKopyası olusturuluyor")
            karar = "1"
            i_soket.sendto(bytes(karar, encoding='utf-8'), (ip, port))
            print("\nDosya sunucuya yuklendi.")
    else:                                                                                   
        print("\nBu isimde bir dosya istemcide bulunamadi.")
elif(tercih == 3):
    dosyaIsmi = input("\nDosya ismini girin: ")
    i_soket.sendto(bytes("get yap", encoding='utf-8'), (ip, port))
    i_soket.sendto(bytes(dosyaIsmi, encoding='utf-8'), (ip, port))       
    kontrol = i_soket.recvfrom(4096)                                              
    if(kontrol[0].decode("utf-8") == "dosya mevcut"):                                            
        dosyaIcerigi, sunucuAdres = i_soket.recvfrom(4096)
        dosyaYukle(dosyaIsmi, dosyaIcerigi)                                                                                                                                                                                
        print("\nDosya istemciye yuklendi.")
    else:                                                                               
        print("\nGirdiginiz isimde bir dosya sunucuda mevcut degil.")
elif(tercih == 4):
    i_soket.sendto(bytes("bitir", encoding='utf-8'), (ip, port))      
    i_soket.close()                                                                   
    print("\nIstemci sonlandirildi.\n")
    sys.exit()
else:
    print("\nHatalı tercih! \n\n")
    sys.exit()
