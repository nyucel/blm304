#Yiğitcan ÜSTEK-160401030 client.py


import socket
import sys
import time
import os

HOST = sys.argv[1]
PORT = 42 
buf = 65000


def put(client,file_name,host,port):
    
    db = 0
    with open(file_name, 'rb') as f1:
        db = len(f1.read())
    with open(file_name, 'rb') as f:          #put
        client.sendto(bytearray("{0} {1}".format(db,file_name),'utf-8'), (host,port))
        data = f.read(buf)
        client.sendto(data, (host,port))
        while (data):
            client.sendto(data, (host,port))
            data = f.read(buf)
            time.sleep(0.1)





def listele(client,host,port):
    print("-------SUNUCUDAKİ DOSYALAR--------")
    
    i=0 
    print("Komut bekliyor")
    iter,addr = client.recvfrom(buf)
    client.sendto('LIST'.encode(), (host,port))
    while (i < int(iter.decode())):
        data,addr = client.recvfrom(buf)
        print("[" + data.decode() + "]", end =' ')
        i+=1
    print("")

def get(client,filename,host,port):
    try:
        client.settimeout(10)
        i = 0
        d,addr = client.recvfrom(buf)
        print("Gelen veri: {0}\tAdres:{1}\n".format(d.decode() ,addr) )
        len_d = int(d.decode().split(" ")[0])
        db = len_d
    
        data_len = int(len_d / buf)
        with open(filename , 'wb') as f:        
            data,addr = client.recvfrom(buf)
            while (i < data_len+1 ):
                data, addr = client.recvfrom(buf)
                f.write(data)
                i +=1
        os.chmod(filename, 0o436 ) #Gelen dosyanın sadece okunabilir moddan çıkarıyoruz
    except:
        with open(filename, 'rb') as f2:
            len1 = len(f2.read())
        if (db != len1):
            print("Bağlantı kesintiye uğratılmış!")
            client.close()
            exit(1)






with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    
  
    


    while(1):
        try:
            try:
                time.sleep(1)
                client.sendto('LIST'.encode(),(HOST,PORT))
                listele(client,HOST,PORT) 
            except socket.timeout:
                print("Veri yollanamadı") 

            liste = os.listdir(os.getcwd())
            print("------YERELDEKİ DOSYALAR-----") 
            for i in liste:
                print("[" + i + "]" ,end=' ' )
            print("")
            inp1 = input("\nKomutu giriniz(Yardım için help yazınız):")
            inp = inp1.split(" ")[0]
            
            if inp == 'PUT':
                try:
                    
                    inp = inp1.split(" ")[1]
                    client.sendto('PUT'.encode(), (HOST,PORT))
                    put(client,inp,HOST,PORT)
                    inp = ''
                except socket.timeout:
                    print("Veri yollanamadı\n")
            elif inp == 'GET':
                try:
                    client.sendto('GET'.encode(),(HOST,PORT))
                    inp = inp1.split(" ")[1]
                    client.sendto(inp.encode(), (HOST,PORT))
                    get(client,inp,HOST,PORT)
                    inp = ''
                except socket.timeout:
                    print("Veri alınamadı\n")
            elif inp == 'LIST':
                
                try:
                    client.sendto('LIST'.encode(),(HOST,PORT))
                    inp = ''
                    listele(client,HOST,PORT) 
                except socket.timeout:
                    print("Veri yollanamadı\n")    
            elif inp == 'exit':
                client.sendto('exit'.encode(), (HOST,PORT))
                client.close()
                exit(1)

            else:
                print("PUT komutu için: PUT [dosya_adı]\nGET komutu için: GET [dosya_adı]\nListeleme için:LIST\n Çıkma komutu için:exit\n")
                inp = ''
        except socket.timeout:
            print("Bağlantı zaman aşımına uğradı!")
