#!/usr/bin/python3
# Ahmet Faruk Albayrak - 170401001
import scapy
import os
import sys
import socket
import time

port = 42
ip = input("Lutfen bir sey girmeden enter'a basiniz.")
#ip = 'localhost'
# TODO: automate this
buf = 1024

# Creating server folder
dirName = "sunucu_dosyalari"
if not os.path.exists(dirName):
	os.mkdir(dirName)
	print(dirName, "klasoru olusturuldu.")
else:
	print(dirName, "klasoru zaten var.")
os.chdir(dirName)

while(True):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# udp soket objesi: s
    time.sleep(.5) 	# bu gecikme objenin duzgun olusmasi icin
    s.bind((ip,port))
    #a = input("devammi?: ")
    #if a != '1':
    #	sys.exit()
    print("Sunucu dinlemede...")
    received_bytes = s.recvfrom(buf)        # istemciden veri bekleniyor
    #print(received_bytes[0])
    #print(received_bytes[1])

    client_message = received_bytes[0].decode()    #
    print(client_message)
    client_address = received_bytes[1]
    request = client_message[:3]
    filename= client_message[4:]

    if request == '999':
        ack = str.encode("Sunucu cevirimici.")
        s.sendto(ack, client_address)

    if request == 'dir':
        response = str.encode(str(os.listdir()))
        s.sendto(response, client_address)

    if request == 'GET':
        directory = os.listdir()
        time.sleep(0.1)
        if filename in directory:
            send_this_file_name = filename.encode()
            s.sendto(send_this_file_name, client_address)

            f = open(filename,"rb")
            data = f.read(buf)
            s.sendto(data, client_address)

            while (data):
                if(s.sendto(data, client_address)):
                    print ("Dosya gonderiliyor. Lutfen bekleyiniz...")
                    data = f.read(buf)
                    time.sleep(0.01)

            try:
                s.settimeout(5)
                kontrol = s.recvfrom(buf)[0].decode()

                if(kontrol == 'True'):
                    print('Dosya basariyla gonderildi.')
            except socket.timeout:
                print('Dosya gonderilemedi.')

            s.close()
            f.close()

        else:
            s.sendto(b'hata', client_address)
            s.close()

    if request == 'PUT':
        data = s.recvfrom(buf)[0]
		
        f = open(data.strip(),'wb')
        data = s.recvfrom(buf)[0]
        try:
            while(data):
                data = s.recvfrom(buf)[0]
                f.write(data)
                s.settimeout(10)             # 7 sn boyunca hic veri gelmezse dosya bu kadar heralde diyip dosyayi kapatiyoruz.
        except socket.timeout:
            f.close()
        s.sendto(b'True', client_address)
        s.close()
