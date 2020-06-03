#Mehmet Salih ÇELİK - 170401073
import socket
import os
import sys
import time

sunucu_ip=str(socket.gethostbyname(socket.gethostname()))
sunucu_port=42
sunucu=(sunucu_ip,sunucu_port)
buffer=32768
sunucu_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sunucu_socket.bind(sunucu)
#buffer boyutum 32KB

print("SUNUCU HAZIR")
print("SUNUCU IP ADRESI : ",sunucu_ip)

#paketleri okunabilir hale getirmek ve gonderebilmek icin encode ve decode islemleri
def decode_yap(x):
    return x.decode("utf-8")

def encode_yap(x):
    return x.encode("utf-8")

#sunucu_dosyalari adli klasordeki dosyalari listeliyor.
def listele():
    x = os.listdir("sunucu_dosyalari")
    y = "--- SUNUCUDA BULUNAN DOSYALAR --- "
    for i in range(len(x)):
        y += "\n {}".format(str(x[i]))
    return encode_yap(y)

while 1:
    mesaj,istemci_ip=sunucu_socket.recvfrom(buffer)
    mesaj = decode_yap(mesaj)

    sunucu_socket.sendto(listele(),istemci_ip)
    mesaj, istemci_ip = sunucu_socket.recvfrom(buffer)
    mesaj = decode_yap(mesaj)

    if mesaj=="1":
        continue

    if mesaj[:3]=="GET":
        dosya_boyutu = str(os.stat("sunucu_dosyalari/"+mesaj[4:])[6])
        dosya_boyutu=encode_yap(dosya_boyutu)
        sunucu_socket.sendto(dosya_boyutu, istemci_ip)

        f=open("sunucu_dosyalari/"+mesaj[4:],"rb")
        data=f.read(buffer)
        while data:
            sunucu_socket.sendto(data, istemci_ip)
            print("Dosya yollaniyor")
            data = f.read(buffer)
            time.sleep(0.3)
        f.close()
        print("DOSYA YOLLANDI")

    elif mesaj[:3]=="PUT":
        f=open("sunucu_dosyalari/"+mesaj[4:],"wb")
        veri,adres=sunucu_socket.recvfrom(buffer)
        dosya_boyutu=int(veri.decode("utf-8"))
        print("sunucuya yuklenecek dosyanin boyutu : ",dosya_boyutu,"byte")
        boyut_kontrol=0
        while True:
            if ((boyut_kontrol*buffer)<dosya_boyutu):
                sunucu_socket.sendto("kontrol".encode("utf-8"), istemci_ip)
                yenimesaj, istemci_ip = sunucu_socket.recvfrom(buffer)
                f.write(yenimesaj)
                print("Dosya aliniyor...")
                boyut_kontrol += 1
            else:
                f.close()
                break
        print("DOSYA ALINDI.")
        f.close()

sunucu_socket.close()
print("-----SUNUCU KAPANDI-----")
