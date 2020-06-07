

#Ramazan ŞAHİN  170401069

#CLIENT

import socket,time,os,sys
import platform

def a():
	path = os.getcwd()              
	return str(os.listdir(path))

if __name__ == "__main__":
    ######## Isletim sistemi kontrolu ########
    os_inf = platform.system()
    if os_inf == "Linux":
        os.system("clear")
    elif os_inf == "Windows":
        os.system("cls")
    print("Istemci\n")


HOST = str(input("[*] Ip Adresini Giriniz -> "))
PORT = 42
SİZE=1024
ADDR=(HOST,PORT)
main_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

data = " [*][*]Merhaba Ben İstemci [*][*]"
main_client.sendto(bytes(data,encoding="utf-8"),ADDR)

data,address = main_client.recvfrom(SİZE)
data=data.decode('utf-8').strip()
print("[+] server dosyaları =>" +data)

secim = str(input("[*] Yapılacak işlemi Ve Dosya İsmini Giriniz : "))
liste=[]
liste=secim.split()
secim = liste[0]


if secim == "get" or secim =="GET":
    main_client.sendto(bytes(secim,encoding="utf-8"),ADDR)
    dosya_ismi = liste[1]
    main_client.sendto(bytes(dosya_ismi,encoding="utf-8"),ADDR)

    a,b= main_client.recvfrom(SİZE) # while ın içindeki sendto ya karşılık gelen       
    f = open(dosya_ismi,'wb')
    try:
        while a:
            
            f.write((a))
            main_client.settimeout(1)
            a,b=main_client.recvfrom(SİZE)
            
    except socket.timeout:
        f.close()
        print("[+][+] Dosya Başarılı Bir Şekilde Aktarıldı [+][+]")
       

if secim == "put" or secim == "PUT":
    main_client.sendto(bytes(secim,encoding="utf-8"),ADDR)
    dosya_ismi=liste[1]
    main_client.sendto(bytes(dosya_ismi,encoding="utf-8"),ADDR)
    new_file = open(dosya_ismi,"rb")
    i = new_file.read(1024)
    
    while i:
        main_client.sendto(i,ADDR)
        i = new_file.read(1024)
    print("[+][+] Dosya Başarılı Bir Şekilde Aktarıldı [+][+] ")
    new_file.close()



