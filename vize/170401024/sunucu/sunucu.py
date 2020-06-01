import socket
import os
import time

host = input("Sunucu ip adresini girin: ")
port = 42

print("Servera bağlanıldı.")
print(f"{port}. port dinleniyor.")

def put(s):
    dosyaAdi,adrss=s.recvfrom(4096)
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
    
def get(s):
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
    else:
        s.sendto('notFound', address)

while (True):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    komut,address= s.recvfrom(4096)
    kmt = komut.decode()
    
    if ( kmt[:4].lower() == "list"):
        fileList = str(os.listdir())
        file = fileList.encode('utf-8')
        s.sendto(file, address)

    elif (kmt[:3].lower() == 'get'):
        get(s)
            
    elif (kmt[:3].lower() == 'put'):
        put(s)
    else:
        print("Yanlış komut.")
