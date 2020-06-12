#170401022 Cihan PAR
import socket
from os import listdir

def listeleme():
    print("Dosyalar : \n ------------------")
    dosyalar = " "
    for i in listdir():
        dosyalar += i +"\n"
    return dosyalar
        
def veriyolla(veri, adres):
    try:
        udp_socket.sendto(veri.encode("utf-8"), adres)
    except:
        print("Bağlantı hatası!")

def verial():
    try:
        alinanveri, adr =udp_socket.recvfrom(sizeofudp)
        return alinanveri.decode("utf-8")
    except:
        print("Bağlantı hatası!")

udp_ip=input("ip adresini giriniz : ")
udp_port=42
address=(udp_ip, udp_port)
sizeofudp=4096

udp_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print("Client: Bağlantı isteniyor.")
veriyolla(("Client: Bağlantı isteniyor."), address)

server_mesaj=verial()    #bağlantı teyiti
print(server_mesaj)      #bağlantı teyiti



while True:
    server_mesaj=verial()    #server komut istemi alınır.
    print(server_mesaj)      #Serverın komut istemi yazdırılır.
    komut = input("Bir komut giriniz (GET, PUT): ")    #Komut girilir.    
    veriyolla(komut,address)      #Komut, servera gönderilir.        

    
    if komut == "GET": 
        server_mesaj=verial()                   #Liste
        print(server_mesaj)                     #Liste
        
        server_mesaj=verial()                   #Serverın komutu aldığı onaylanır.
        print(server_mesaj)                     #Serverın komutu aldığı yazdırılır.        
               
        
        dosyaismi = input("Client: Dosya adını ve formatını, 'abc.x' biçiminde giriniz:  ")    #Dosya ismi girilir.                              
        veriyolla(dosyaismi, address)     #Dosya ismi servera gönderilir.
        
        

        alinandosya, adr=udp_socket.recvfrom(sizeofudp)
        print("Client: Veri indiriliyor...")
        with open(dosyaismi.encode(),"wb") as dosya:
            dosya.write(alinandosya)
            dosya.close()
        
        server_mesaj=verial()                   
        print(server_mesaj)
                     
    elif komut == "PUT":        
        dosyaisimleri=listeleme()
        print(dosyaisimleri)
        dosyaismi = input("Client: Dosya adını ve formatını, 'abc.x' biçiminde giriniz:  ")
        veriyolla(dosyaismi,address)
        dosya=open(dosyaismi.encode(),"rb").read()
        udp_socket.sendto(dosya, address)
        
        server_mesaj=verial()                   
        print(server_mesaj)
    else:
        print("Client: Hatalı komut girişi!")
        exit()
        

    