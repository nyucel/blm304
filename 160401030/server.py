#Yiğitcan ÜSTEK-160401030 server.py


import socket
import datetime
import os
import stat
import time 

HOST =  socket.gethostbyname(socket.gethostname())
PORT = 42
err = ''
buf = 65000



def get(server):
    try:
        i = 0
        d,addr = server.recvfrom(buf)
        print("Gelen veri: {0}\tAdres:{1}".format(d.decode().split(" ") ,addr) )
        len_d = int(d.decode().split(" ")[0])
        filename = d.decode().split(" ")[1]
        data_len = int(len_d / buf)
        db = data_len
        with open(filename , 'wb') as f:        #GET komutu
            data,addr = server.recvfrom(buf)
            while (i < data_len+1 ):
                data, addr = server.recvfrom(buf)
                f.write(data)
                i +=1
        os.chmod(filename, 0o436 ) #Gelen dosyanın sadece okunabilir moddan çıkarıyoruz
        time.sleep(1)
    except:
        with open(filename, 'rb') as f2:
            len1 = len(f2.read())
        if (db != len1):
            print("Bağlantı kesintiye uğratılmış!")
            server.close()
            exit(1)
            
def listele(server,addr):
    liste = os.listdir(os.getcwd())
    print("Listeleme isteği yapıldı")
    server.sendto("{0}".format(len(liste)).encode(), addr )
    time.sleep(0.5)
    d,addr = server.recvfrom(buf)
    for i in liste:
        server.sendto(i.encode(), addr)
        time.sleep(0.1)
    server.settimeout(30)
        


def put(server,addr,filename):
    db = 0
    try:
        
        with open(filename, 'rb') as f1:
            db = len(f1.read())
        with open(filename, 'rb') as f:          
            server.sendto(bytearray("{0} {1}".format(db,filename),'utf-8'), addr)
            data = f.read(buf)
            server.sendto(data, addr)
            while (data):
                server.sendto(data, addr)
                data = f.read(buf)
                time.sleep(0.1)
    except:
        print("Hata")




while(1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server: #UDP haberleşeceğimizi belirttik
                                                                    
            server.bind((HOST,PORT))  #Host adresi ve Port bilgisi ile haberleşmeyi başlattık
            print("Dinlemeye başlandı: {0}:{1}".format(HOST, PORT))
            
            
            
            addr = server.recvfrom(buf)[1]
            try:
                listele(server,addr)
            except socket.timeout:
                print("Veri alınamadı")

            data,addr = server.recvfrom(buf) 
            print("Gelen İstek:" + data.decode())
            if (data.decode() == 'PUT'):
                get(server)
                
            elif (data.decode() == 'LIST'):
                try:
                    
                    listele(server,addr)
                except socket.timeout:
                    print("Veri alınamadı")
            elif (data.decode() == 'GET'):
                try:
                    print("Dosya adı:",end='')
                    
                    filename,addr = server.recvfrom(buf)
                    
                    print(filename.decode())
                    put(server,addr,filename)
                except socket.timeout:
                    print("Veri yollanamadı")
            elif (data.decode() == 'exit'):
                exit(1)
    except socket.timeout:
        print("...Sonlandırılıyor...")
        server.close()
        exit(1)
    except socket.error:
        print("Sokete bağlanılamadı. Soket açıksa lütfen soketi kapatın!")
        exit(1)
