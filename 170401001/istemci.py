#!/usr/bin/python3
# Ahmet Faruk Albayrak - 170401001
import os
import sys
import base64
import socket
import time
print("istemci, sadece istemci.py dosyasinin bulundugu dizindeki dosyalari gonderebiliyor")

port = 42
host_ip = input ("Sunucunun ipv4 adresini giriniz: ")
#host_ip = '127.0.0.1'
buf = 1024
flag = "999"
#eeflag = base64.b64encode(eflag)	# b64 encoding yapiyoruz ki, txt disinda dosyalar gonderebilelim. TODO. Zaten gonderiliyormus
#print(type(ee))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# udp soket objemiz: s
time.sleep(.1) 	# bu gecikme objenin duzgun olusmasi icin

try: # server online mi? kontrolu
	s.sendto(str.encode(flag), (host_ip, port))
except:
	print('Ya sunucu cevrimdisi ya da IP hatali girildi. Sonlandiriliyor...')
	sys.exit()

responseFromServer = s.recvfrom(buf)
#print("test")
#print(responseFromServer[0].decode())

request = input ("Sunucuya bir komut gonderin(dir, GET file, PUT file, exit): ")
erequest = request.encode()
s.sendto(erequest, (host_ip, port))
if(request.find('GET') == 0):
    data = s.recvfrom(buf)[0]
    if(data.decode() == 'hata'):
        print('Dosya bulunamadi.')
    else:
        f = open(data.strip(),'wb')
        data = s.recvfrom(buf)[0]
        try:
            while(data):
                data = s.recvfrom(buf)[0]
                f.write(data)
                s.settimeout(5)
                print("Lutfen 5sn bekleyiniz.")
        except socket.timeout:
            f.close()
        s.sendto(b'True', (host_ip, port))
        s.close()
elif(request.find('PUT') == 0):
    filename = request[4:]
    files = os.listdir()
    if filename in files:
        file_to_send = filename.encode()
        f=open(filename,"rb")
        data = f.read(buf)
        s.sendto(file_to_send, (host_ip, port))
        s.sendto(data, (host_ip, port))
        while (data):
            if(s.sendto(data, (host_ip, port))):
                print ("Gonderiliyor...")
                data = f.read(buf)
                time.sleep(0.01)
        try:
            s.settimeout(5)
            kontrol = s.recvfrom(buf)[0].decode()
            if(kontrol == 'True'):
                print('dosya gonderildi')
        except socket.timeout:
            print('dosya gonderilemedi')
        s.close()
        f.close()
    else:
        print('Dosya bulunamadi.')

elif(request.find('dir') == 0):
    files = s.recvfrom(buf)
    msg = "Sunucudaki dosyalar: {}".format(files[0].decode())
    print(msg)
    s.close()

elif(request.find('exit') == 0):
    sys.exit()

else:
    print('Gecersiz bir komut girildi.')
