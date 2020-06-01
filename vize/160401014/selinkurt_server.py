#Selin KURT 160401014

import socket
import sys
import os

newsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
udp_port = 42                                  
blocksize = 4096
newsocket.bind(('0.0.0.0',udp_port))

while 1:

    print("server is ready..")
    
    data, address = newsocket.recvfrom(1024)           
    print(data.decode("utf-8"), address)
    
    #dizindeki dosyaların listelenmesi
    pwd_info = os.getcwd()
    pwd_info_list = os.listdir(pwd_info)
    pwd_info_separate = ",".join(pwd_info_list)
    newsocket.sendto(pwd_info_separate.encode(), address) 
    
    veri, address = newsocket.recvfrom(1024)
    metod = veri.decode("utf-8")

    if(metod == "GET"):

        data, address = newsocket.recvfrom(1024)
        data_separate = data[4::] #PUT/GET metodundan sonra yazılan dosya adını ayırmak için
        dosya_adi = data_separate.decode("utf-8")
        
        f = open(dosya_adi, "rb")
        icerik = f.read(blocksize)
        while icerik != '':
            newsocket.sendto(icerik, address) 
            icerik = f.read(blocksize) 
            print("dosya gonderildi.")
            break

    elif(metod == "PUT"):

        contents, address = newsocket.recvfrom(1024)  
        dosya = open("yerelden_sunucuya_yuklenen_dosya.txt", "wb+")
        dosya.write(contents)
        dosya.close()
