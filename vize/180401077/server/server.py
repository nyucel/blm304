# Ercan Berber 180401077

import socket
import os
from os import listdir
from os.path import isfile,join
import select
import time

DATA_SIZE = 0
PATH = f"{os.path.dirname(os.path.abspath(__file__))}/ServerFiles" #Server dosyalarının olduğu yer
HOST = str(socket.gethostbyname(socket.gethostname()+".local")) #Hostun ip adresi
PORT = 42 #Serverın dinleyeceği port
BUFFERSIZE = 4096 #tek seferde gönderilecek veri büyüklüğü, byte cinsinden
TIMEOUT = 3


print(f"Serverın adresi {HOST}")


while True:
    connection=1
    #Serverı başlattık
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #UDP server
    s.bind((HOST,PORT))
    data, addr = s.recvfrom(1024) #Bağlantı bekliyor
    print(addr,"Bağlandı\n") #Bağlananın adresi
    filess=[f for f in listdir(PATH) if isfile(join(PATH,f))] #Server dosyalarını listeye ekliyoruz.
    s.sendto(str(filess).encode(),addr) #Server dosyalarını clienta yolluyoruz.
    while connection==1:

        msg = s.recv(BUFFERSIZE) #Komut geldi
        if msg.decode().lower()=="exit": #Clientdan EXIT komutu gelmiştir.a
            print(f"{addr} Çıktı")
            break
        komut,data = msg.decode().split(" ") #İkiye böldük

        if komut.lower()=="put": #Clientdan PUT komutu gelmiştir.
            DATA_SIZER=s.recv(BUFFERSIZE).decode() #Gelen dosyanın boyutu, sondaki R=Received.
            if data:
                file_name = data
                print(f"{file_name} Servera yükleniyor...")
            f = open(PATH+"/"+file_name, 'wb') #Dosyayı oluşturduk.
            while True:
                ready = select.select([s], [], [], TIMEOUT)
                if ready[0]:
                    data = s.recv(BUFFERSIZE)
                    f.write(data) #Gelen veriyi dosyaya yazdık.
                else:
                    f.close()
                    DATA_SIZE=str(os.stat(PATH+"/"+file_name).st_size)
                    if(DATA_SIZE==DATA_SIZER):
                        print(f"{file_name} Servera yüklendi!")
                        s.sendto("1".encode(),addr)
                    else:
                        print(f"{file_name} Eksik yüklendi")
                        print("İstemci ile bağlantı sonlandı")
                        connection=0
                    print("----------------------------------------------")
                    break

        if komut.lower()=="get": #Clientdan GET komutu gelmiştir.
            while True:
                file_name=data
                try:
                    f=open(PATH+"/"+file_name,"rb") #Dosyayı okumayı deniyoruz.
                except FileNotFoundError: #Böyle bir dosya yok ise.
                    s.sendto("0".encode(),addr)
                    break #Dosya olmadığı için çıkıyoruz.
                print(f"{file_name} Yollaniyor...")
                s.sendto("1".encode(),addr) #Önce dosyanın olduğunu haber ediyoruz.
                DATA_SIZE=os.stat(PATH+"/"+file_name).st_size
                s.sendto(str(DATA_SIZE).encode(),addr)
                data=f.read(BUFFERSIZE) #BUFFERSIZE kadar okuyoruz.
                while(data): #Data varsa.
                    if(s.sendto(data,addr)):
                        data=f.read(BUFFERSIZE) #Okumaya devam ediyoruz.
                        time.sleep(0.002)
                f.close()
                try:
                    durum=s.recv(BUFFERSIZE).decode()
                except ConnectionResetError:
                    print("Bağlantı Koptu")
                    print(f"{addr} Çıktı")
                    connection=0
                    break
                print(f"{file_name} Gönderildi!")
                print("----------------------------------------------")
                break