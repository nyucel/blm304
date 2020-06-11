import socket
import os
import sys
import time

def get(s):
    dosyaAdi,adrss=s.recvfrom(4096)
    if (dosyaAdi.decode('utf-8') == 'notFound'):
        print('Aranılan dosya bulunamadı.')
    else:
        f = open(dosyaAdi, 'wb')  
        dosyaVeri,adrs = s.recvfrom(4096) 
        try:
            while (dosyaVeri):
                dosyaVeri=s.recv(4096)
                f.write(dosyaVeri)
                s.settimeout(2)
                s.sendto(('True').encode(),adrss)
        except socket.timeout:
            f.close()
        #s.sendto('True', adrss)
        s.close()

def put(s):
    dosyalar = os.listdir()
    if kmt[4:] in dosyalar:
        dosyaAdi = kmt[4:].encode('utf-8')
        s.sendto(dosyaAdi, address) 
        with open(kmt[4:],"rb") as f:
            a = f.read(4096)
            s.sendto(a,address)
            while(a):
                if(s.sendto(a,address)):
                    a=f.read(4096)
                    time.sleep(0.02)
                    try:
                        s.settimeout(1)
                        data,adrs = s.recvfrom(4096)
                        pDurum = data.decode('utf-8')
                        print(pDurum)
                        if (pDurum == 'True'):
                            print('Dosya gonderildi')
                    except socket.timeout:
                        print('Dosya gonderimi basarisiz')

        


host = input("Sunucu ip adresini girin: ")
address = (host, 42)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

kmt = "list"
Listkmt = kmt.encode('utf-8')
try:
    s.sendto(Listkmt, address)

except:
    print('Baglanti hatasi')
    sys.exit()

message, addr = s.recvfrom(4096)
msg = message.decode('utf-8')
dosyaListe = "Dosyalar: {}".format(msg)
print(dosyaListe)

komut = input("Sunucudan dosya yüklemek için: get dosya_adi\nSunucuya dosya yüklemek için: put dosya_adi\n")
kmt = komut.encode()
s.sendto(kmt, address)
if (komut[:3].lower() == 'get'):
    get(s)
    
elif(komut[:3].lower() == 'put'):
    put(s)
    
else:
    print('Hatalı komut.')
