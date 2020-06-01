#Selin KURT 160401014

import socket
import sys

newsocket= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      
udp_port = 42			        
blocksize = 4096
ip_address = input("IP adresi giriniz: ")

while 1:
    try:
        metin ="..Baglanti basarili.."
        newsocket.sendto(metin.encode(),(ip_address,udp_port))
    except:
        print("..Baglanti basarisiz..")
        sys.exit()

    dosya_listesi, address = newsocket.recvfrom(1024) 
    print("Dosyalar listeleniyor:", dosya_listesi.decode("utf-8"),"\n")
    komut = input("GET dosya_adi ile sunucudaki dosyayi indirin veya PUT dosya_adi ile yerelinizdeki dosyayi sunucuya yukleyin\n")
    
    metod = komut[0:3] #Girilen put/get metodu ayrılır 
    dosya_adi = komut[4::] #Girilen dosya adı ayrılır

    if(metod == "PUT"):

        newsocket.sendto(metod.encode(),(ip_address,udp_port))
    
        f = open(dosya_adi, "rb")
        paket = f.read(blocksize)
        while paket != '':
            try:
                newsocket.sendto(paket,(ip_address,udp_port))
            except:
                print("Dosya gönderilemedi")
                sys.exit()
            paket = f.read(blocksize)
            break                            
        
    elif(metod == "GET"):

        newsocket.sendto(metod.encode(),(ip_address,udp_port))
        newsocket.sendto(komut.encode(),(ip_address,udp_port))

        try:
            data, address = newsocket.recvfrom(1024)
        except:
            print("Dosya cekme basarisiz")

        dosya = open("sunucudan_gelen_dosya.txt", "wb")
        dosya.write(data)
        dosya.close() 
