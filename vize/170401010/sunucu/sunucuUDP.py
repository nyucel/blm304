#Baran Akçakaya 170401010
#Veri Haberleşmesi Vize
import socket
import os
import time

#UDP_IP = "192.168.0.0"#socket.gethostbyname(socket.gethostname())
UDP_IP = str(input("Sunucu IP adresi:"))
UDP_PORT = 42
buffer = 4096

location = os.getcwd()              #Bulundugum lokasyonu yazdırıyorum
example = str(os.listdir())         #Lokasyondaki dosyaları yazdırıyorum
#LFC = pickle.dumps(example)
LFC = example.encode()
klasör_name = 'SunucuD'
alindimi = 0

if(klasör_name not in example):
        os.mkdir(klasör_name)       #Böyle bir klasör yoksa oluşturuyorum.
os.chdir(location+"\SunucuD")


message="Dosyalar listeleniyor..."
print("Sunucu açıldı kanal dinleniyor.")

while True:
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    sock.bind((UDP_IP, UDP_PORT))
    
    location = os.getcwd()
    example = str(os.listdir())
    LFC = example.encode()
    
    data, addr = sock.recvfrom(1024)
    print("-----------------------------------")
    print('Cihaz IP:',addr[0])
    print('Cihaz PORT:',addr[1])
    print("Gelen mesaj:",data)
    sock.sendto(LFC,addr)
    komut,addr2 = sock.recvfrom(1024)
    print("Gelen Komut:",komut)
    komut = komut.decode()
    komut = komut.split(' ')
    
    if('get' == komut[0].lower()):
        print("Dosya hazırlanıyor.")
        file = open(komut[1].encode(),'rb')
        veri = file.read(buffer)
        while(veri):
            if(sock.sendto(veri,addr2)):
                print("Veri gönderiliyor...")
                try:
                    veri5,addr5=sock.recvfrom(1024)
                    sock.settimeout(3)
                    if("True"!=veri5.decode()):
                            alindimi= 1
                            break
                except socket.timeout:
                    print("Bağlantı sağlanamadı")
                    alindimi = 1
                    break
                veri = file.read(buffer)
                time.sleep(0.01)
        if(alindimi == 0):
            print("Dosya Gönderildi.")
            file.close()
        else:
            print("Dosya Gönderilemedi.")
            file.close
            alindimi = 0
            
    elif('put' == komut[0].lower()):
        veri3,addr3 = sock.recvfrom(buffer)
        file2 = open((komut[1]).strip(),"wb")
        try:
            while(veri3):
                print("Dosya alınıyor...")
                sock.sendto('True'.encode(),addr3)
                file2.write(veri3)
                veri3,addr3 = sock.recvfrom(buffer)
                sock.settimeout(3)
        except socket.timeout:
            print("Dosya alındı.")
            file2.close()
    