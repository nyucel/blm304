#Erdin Alhas 150401052

import os
import sys
import time
from socket import *
from os import system, name
ip = '127.0.0.1'
port = 42                                                       
s_soket = socket(AF_INET, SOCK_DGRAM)
s_soket.bind((ip, port))
print("\nSunucu Hazir\n")
kontrol, istemciAdres = s_soket.recvfrom(4096)
s_soket.sendto(bytes("Sunucu hazir", encoding='utf-8'), istemciAdres)         
i, istemciAdres = s_soket.recvfrom(4096)                                       
if(i.decode("utf-8") == "listeleme yap"):
    dosyalar = "\n".join(os.listdir())                                                  
    s_soket.sendto(bytes(dosyalar, encoding='utf-8'), istemciAdres)   
    sys.exit()             
elif(i.decode("utf-8") == "put yap"):
        cevap = s_soket.recvfrom(4096)                                                 
        if(cevap[0].decode("utf-8") == "mevcut"):                                          
            dosyaIsmi, istemciAdres = s_soket.recvfrom(4096)
            dosyaIcerigi = s_soket.recvfrom(4096)
            if(os.path.exists(dosyaIsmi.decode("utf-8")) == True):                           
                s_soket.sendto(bytes("aynisi mevcut", encoding='utf-8'), istemciAdres)
                karar = s_soket.recvfrom(4096)                              
                if(karar[0].decode("utf-8") == "1"):                                     
                    yeniAd = dosyaIsmi.decode("utf-8")[:-4] + " (kopya)" + ".txt"
                    dosyaYeni = open(yeniAd, "wb")
                    dosyaYeni.write(dosyaIcerigi[0])
                    dosyaYeni.close()
                print("\nPUT islemi basariyla gerceklesti..")
            else:                                                                          
                dosyaYeni = open(dosyaIsmi, "wb")
                dosyaYeni.write(dosyaIcerigi[0])
                dosyaYeni.close()
                s_soket.sendto(bytes("tamam", encoding='utf-8'), istemciAdres)
                print("\nPUT islemi basariyla gerceklesti..")
        else:                                                                             
            print("\nGirilen adda bir dosya istemcide bulunamadi..")
elif(i.decode("utf-8") == "get yap"):
    dosyaIsmi, istemciAdres = s_soket.recvfrom(4096)
    if (os.path.exists(dosyaIsmi.decode("utf-8")) == True):                                               
        dosya = open(dosyaIsmi.decode("utf-8"), "rb")
        s_soket.sendto(bytes("dosya mevcut", encoding='utf-8'), istemciAdres)
        dosyaIcerik = dosya.read()
        dosya.close()
        s_soket.sendto(dosyaIcerik, istemciAdres)
        kontrol = s_soket.recvfrom(4096)                                           
        print("\nGET islemi basariyla gerceklesti..")
        sys.exit()
    else:                                                                               
        print("\n! Bu isimde bir dosya sunucuda mevcut değil")
        sys.exit()
elif(i.decode("utf-8") == "bitir"):
    s_soket.close()                                                                
    print("\nSunucu kapandi")
    sys.exit()