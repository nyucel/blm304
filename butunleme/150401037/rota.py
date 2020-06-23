#150401037 HAKAN DURMAZ
import sys
import random
import socket
hedef_adres = sys.argv[1]
hedef_ip = socket.gethostbyname(hedef_adres)                #Sunucunun adından dns sorgusu yapıyor.
print("Girdiginiz ip adresi: " +hedef_adres)
print("Girdiginiz adresin DNS sorgusu: "+hedef_ip)
f = open("rota.txt","w")                                     #Dosya oluşturuyor.
timeout = 0.2
ttl=1                                                        #var olan ttl'i 1 olarak alıyor.
port = random.choice(range(1024, 65100))                     #Random port numarası alıyor.
while True:
     receiver = socket.socket(family=socket.AF_INET,type=socket.SOCK_RAW,proto=socket.IPPROTO_ICMP) 
     receiver.settimeout(timeout)                                                                        #Receiver Tanımlıyor.
     receiver.bind(('',port))                                                                       
     
     sender = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM,proto=socket.IPPROTO_UDP)  
     sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)                                                #Sender Tanımlıyor.
     sender.sendto(b'',(hedef_ip,port))
     
     adres = None
     
     try:
          data, adres = receiver.recvfrom(512)         #Makineden cevap bekliyor.
                    
     except socket.error:          #Soketlerin hata vermesi durumunda ekrana * basıyor.
          print("Islem devam ediyor.")
          
     finally:                      
          receiver.close()         #Soketleri kapatıyor.
          sender.close()

     if(str(adres) == 'None'):     #Eğer ulaştığımız makine cevap vermiyorsa yıldız koyup alt satıra geçiyor.
          f.write("\n*")
     
     
     if(str(adres) != 'None'):     #Eğer ulaştığımız makine hedef makine değilse dosyaya yazıyor.
          f.write("\n" +str(adres[0]))
     
          
     ttl += 1
     if(ttl>30):
          print("Islem tamamlandi.")                       #TTL Degeri 30'u geçtiğinden programdan çıkıyor.
          break
    









    
