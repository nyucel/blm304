#Baran Akçakaya 170401010
#Veri Haberleşmesi Vize
import socket
import os
import time

#UDP_IP = "192.168.0.0"#socket.gethostbyname(socket.gethostname())
UDP_IP = str(input("Lütfen Sunucunun IP adresini girin:"))
UDP_PORT = 42
MESSAGE = "Hello, Server!"      #Bağlantı kurulduğunuanlamak için Mesaj gönderiyorum
buffer = 4096

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("Message:", MESSAGE)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      #AF_INET = IPV4,SOCK_DGRAM=UDP
sock.sendto(MESSAGE.encode(),(UDP_IP,UDP_PORT))
try:
    msg,adr=sock.recvfrom(1024)
    sock.settimeout(3.0)            #3 saniye icinde mesaj alınmassa hata mesajı yazdırıyorum.
    #msg = pickle.loads(msg)
    msg = msg.decode()
except sock.timeout:
    print("REQUEST TIME OUT")

print("\nDosyalar Listeleniyor:")
msg = msg[1:-1]
msg = msg.split(', ')     #gelen mesajı alt alta yazdırmak için ayırıyorum
tutucu = 0
tutucu2 = 0

def dosya_al(veri_adi,sock):
    veri,adr2 = sock.recvfrom(buffer)
    file = open((veri_adi).strip(),"wb")    #Dosya acıyorum
    try:
        while(veri):
            print("Dosya alınıyor...")
            sock.sendto('True'.encode(),adr2)   #Her veri alındıktan sonra alındı bilgisi gönderiyorum
            file.write(veri)
            veri,adr2 = sock.recvfrom(buffer)
            sock.settimeout(2)
    except socket.timeout:
        print("Dosya alındı.")
        file.close()
        
def dosya_gönder(sock,dosya_name,adr):
    alindimi = 0
    print("Dosya hazırlanıyor.")
    file = open(dosya_name.encode(),'rb')
    veri2 = file.read(buffer)
    while(veri2):
        if(sock.sendto(veri2,adr)):
            print("Veri gönderiliyor...")
            try:
                veri5,adr5=sock.recvfrom(1024)
                sock.settimeout(3)
                if("True"!=veri5.decode()):   #Dosya alındımı diye kontrol ettiriyorum
                        alindimi = 1
                        break
            except socket.timeout:
                print("Bağlantı sağlanamadı")
                alindimi = 1
                break
            veri2 = file.read(buffer)
            time.sleep(0.01)
    if(alindimi == 0):
        print("Dosya Gönderildi.")
        file.close()
    else:
        print("Dosya Gönderilemedi.")
        file.close
        alindimi = 0

while(tutucu2 == 0):
    for files in msg:
        print(files)
    
    inp = str(input("Lütfen işlem giriniz:"))
    kontrol = inp.split(' ')
    if(len(kontrol)!=2):
        print("Komut iki kelime olmalı.EXP: GET Dosya_adı\n")
    else:
        if('get'==kontrol[0].lower()):
            for z in msg:
                if(z[1:-1] == kontrol[1]):
                        sock.sendto(inp.encode(),adr)
                        tutucu = 1
                        tutucu2 = 1
                        break
            if(tutucu == 1):
                print("Komut Gönderildi.")
                dosya_al(kontrol[1],sock)
                tutucu = 0
            else:
                print("Böyle bir dosya yok!\n")
        elif("put"==kontrol[0].lower()):
            location = os.getcwd()
            example = str(os.listdir())
            LFC = example[1:-1]
            LFC = LFC.split(", ")
            for n in LFC:
                if(kontrol[1] == n[1:-1]):
                        sock.sendto(inp.encode(),adr)
                        tutucu = 1
                        tutucu2 = 1
                        break
            if(tutucu == 1):
                print("Komut Gönderildi.")
                dosya_gönder(sock,kontrol[1],adr)
                tutucu = 0
            else:
                print("Böyle bir dosya yok!\n")
        else:
            print("Hata! Lütfen GET yada SET komutu giriniz.\n")
            
