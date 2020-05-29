import socket
import os
import time
#Enes Nurullah Kendirci
localIP = input("sunucu IP adresini girin")

localPort = 42                                                      #istenen sabit port
bufferSize = 4096
 
anaKlasor = os.listdir()                                            #sunucudaki islemleri yapacagimiz klasoru olusturduk
sD = 'sunucudakiDosyalar'
if sD not in anaKlasor:
    os.mkdir(sD)
    print("sunucudakiDosyalar klasörü oluşturuldu")
else:
    print("klasör zaten var")
os.chdir(sD)
 

while(True):                                                        #Serverin kapanmamasi icin
    
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# internet/UDP
    
    UDPServerSocket.bind((localIP, localPort))                      #Bind to address and ip
    
    i = 0
    while(i < 1):                                                   # anlamadığım bir sorunu çözmek için uyguladım 26, 27, 80
        
        print("Server dinlemede")
        
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)     #istemciden gelen komutu bekleme
    
        message = bytesAddressPair[0].decode()                      #gelen verinin mesaj(komutu) kısmını aldık
        
        address = bytesAddressPair[1]                               #istek gelen istemcinin adresi
        
        komut = message[:3]                                         #uygun formatta gelen mesajı böldük
        dosyaAdi = message[4:]                                      
        
        if(komut == '917'):                                         #917 benim belirdiğim dosyaları listele komutu(ipucu olarak istemcide verilmemiştir). Istemci tarafından gelen ilk istek kesinlikle budur
            msgFromServer = str(os.listdir())                       #sunucudaki dosyalarin isimlerini mesajımıza ekledik
            
            bytesToSend = str.encode(msgFromServer)                 #göndermek için encode uyguladik
            
            UDPServerSocket.sendto(bytesToSend, address)            #sunucudaki dosyalarin isimlerini aldigimiz(35) adrese yolladik
        
        elif(komut == 'GET'):                                       # sunucu[data] -> istemci
            
            klasordekiDosyalar = os.listdir()                       #dosya bulunursa
            if dosyaAdi in klasordekiDosyalar:                      
                
                file_name= dosyaAdi.encode()                        #dosyaAdini gonderilmeye hazirladik
    
                f=open(dosyaAdi,"rb")                               #yollanacak dosyayi hazirladik
                data = f.read(bufferSize)
                
                UDPServerSocket.sendto(file_name, address)          #dosya ismini yolladik
                
                UDPServerSocket.sendto(data, address)               #dosyayi yolladik
                while (data):                                           
                    if(UDPServerSocket.sendto(data, address)):
                        print ("sending ...")
                        data = f.read(bufferSize)
                        time.sleep(0.01)
                
                try:                                                #dosyanin iletildi bilgisini bekledik
                    UDPServerSocket.settimeout(3)
                    kontrol = UDPServerSocket.recvfrom(bufferSize)[0].decode()
                    
                    if(kontrol == 'True'):                          #iletilme durumunu yazdirdik
                        print('dosya gonderildi')
                except socket.timeout:
                    print('dosya gonderilemedi')
                    
                UDPServerSocket.close()                             #dosyalari bellekte yer kaplamamasi icin kapattik
                f.close()
            
            else:                                                   #dosya yoksa
                UDPServerSocket.sendto(b'error', address)
                UDPServerSocket.close()
                
        elif(komut == 'PUT'):                                       #sunucu <- istemci[data]
            
            data = UDPServerSocket.recvfrom(bufferSize)[0]          #dosya adini dinledik
            
            f = open(data.strip(),'wb')                             #dosya ismini duzlenleyerek dosyayi actik
            
            data = UDPServerSocket.recvfrom(bufferSize)[0]          #dosyamizin icerigini dinliyoruz
            try:                                                    
                while(data):
                    data = UDPServerSocket.recvfrom(bufferSize)[0]
                    f.write(data)
                    
                    UDPServerSocket.settimeout(3)                   #belirlenen süre veri gelmezse dinlemeyi birakiyoruz
            except socket.timeout:
                f.close()
               
            UDPServerSocket.sendto(b'True', address)                #verinin alindigi bilgisini gonderiyoruz
            UDPServerSocket.close()
            
        i += 1