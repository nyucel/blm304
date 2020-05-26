import socket
import os
import sys
import time
#Enes Nurullah Kendirci
ip = input("sunucu IP adresini girin")                              #sunucu IPsini okuduk
serverAddressPort   = (ip, 42)                                      
bufferSize          = 4096

msgFromClient       = "917"                                         #dosyalari listelemesi benim belirledigim komut(detay icin sunucu.py satir 40)

bytesToSend         = str.encode(msgFromClient)                     #komutu gondermek icin encode ile hazirdik

UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # internet/UDP

try:
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)          #ilk komutuz olan '917'yi yolladik

except:                                                             #sunucuya baglanilmadigindan kodu durdurduk
    print('sunucuya baglanilamadi ip adresini kontrol edin')
    sys.exit()                                                      
    
msgFromServer = UDPClientSocket.recvfrom(bufferSize)                #talebin karsigilini dinleme

msg = "Yüklenmiş dosyalar {}".format(msgFromServer[0].decode())     #konsolda listeleme
print(msg)

kmt = input("KOMUT GİRİN(GET/PUT DosyaAdı)")                        #belirtilen formatta girdi bekleniyor (orn. PUT deneme.txt)

komut = kmt.encode()                                                #kullanicidan aldigimiz komutu ve dosya hazirladik
UDPClientSocket.sendto(komut, serverAddressPort)                    #ve yolladik

if(kmt.find('GET') == 0):                                           #istemci <- sunucu[data]
        
    data = UDPClientSocket.recvfrom(bufferSize)[0]                  #talep edilen dosyayin ismini dinliyoruz
    
    if(data.decode() == 'error'):                                   #sunucuda dosyayi bulamazsa
        print('dosya bulunamadi')
        
    else:
        f = open(data.strip(),'wb')                                 #gelen isimle dosya actik
        
        data = UDPClientSocket.recvfrom(bufferSize)[0]              #dosyamizin icerigini dinliyoruz
        try:                                                            
            while(data):
                data = UDPClientSocket.recvfrom(bufferSize)[0]
                f.write(data)
                
                UDPClientSocket.settimeout(3)                       #belirlenen süre veri gelmezse dinlemeyi birakiyoruz
        except socket.timeout:
            f.close()
        
        UDPClientSocket.sendto(b'True', serverAddressPort)          #verinin alindigi bilgisini gonderiyoruz
        UDPClientSocket.close()
        
elif(kmt.find('PUT') == 0):                                         #istemci[data] -> sunucu
    
    dosyaAdi = kmt[4:]                                              #input alinan dosya ismini ayirdik
    
    klasordekiDosyalar = os.listdir()                               #dosya varsa
    if dosyaAdi in klasordekiDosyalar:                              
        
        file_name = dosyaAdi.encode()                               #dosyaAdini yollamak icin hazirladik
        
        f=open(dosyaAdi,"rb")                                       #dosyayi python icersinde actik
        data = f.read(bufferSize)
                
        UDPClientSocket.sendto(file_name, serverAddressPort)        #dosya ismini gonderdik
        
        UDPClientSocket.sendto(data, serverAddressPort)             #dosyayi gonderdik
        while (data):
            if(UDPClientSocket.sendto(data, serverAddressPort)):
                print ("gonderiliyor...")
                data = f.read(bufferSize)
                time.sleep(0.01)
        
        try:                                                        #sunucudan dosyanin alindigi bilgisini belirtilen sure beklenir
            UDPClientSocket.settimeout(3)
            kontrol = UDPClientSocket.recvfrom(bufferSize)[0].decode()
            
            if(kontrol == 'True'):                                  #konsolda bilgilendirme yaptik
                print('dosya gonderildi')
        except socket.timeout:
            print('dosya gonderilemedi')
        
        UDPClientSocket.close()
        f.close() 
            
    else:
        print('dosya yok')
        
else:
    print('yanlış bir komut girdiniz!')
    
