# Ercan Berber 180401077

import socket
import time
import sys
import os
import select

DATA_SIZE=0
HOST = str(input("Sunucu IP girin..: "))
PORT = 42 
BUFFERSIZE = 4096 #Tek seferde gönderilecek veri büyüklüğü.
TIMEOUT = 3
PATH=f"{os.path.dirname(os.path.abspath(__file__))}/ClientFiles" #Client dosyalarının olduğu yer.

def get(msg,dosya): #Serverdan indir.
    s.sendto(msg.encode(),(HOST,PORT)) #Dosyanın adını yolladık.
    dene=s.recv(BUFFERSIZE).decode() #Dosya varsa 1 yoksa 0 döndü.
    if dene=="0":
        print("Dosya bulunamadı!")
        return
    if dene=="1":
        f = open(PATH+"/"+dosya, 'wb') #Dosya oluşturduk.
        DATA_SIZER=s.recv(BUFFERSIZE).decode() #Gelen dosyanın boyutu, sondaki R=Received.
        while True:
            ready = select.select([s], [], [], TIMEOUT)
            if ready[0]:
                data= s.recv(BUFFERSIZE)
                f.write(data) #Gelen veriyi dosyaya yazdık.
            else:
                f.close()
                DATA_SIZE=str(os.stat(PATH+"/"+dosya).st_size) #İnen dosyanın boyutu.
                if DATA_SIZE==DATA_SIZER:
                    print(f"{dosya} İndirildi!")
                    s.sendto("1".encode(),(HOST,PORT))
                else:
                    print(f"{dosya} Başarı ile indirilemedi.")
                    print("Server bağlantısı sonlandırıldı.")
                    exit()
                break

def put(msg,dosya): #Servera yolla.
    file_name = dosya
    try:
        f = open(PATH+"/"+file_name, "rb") #Dosyayı okumayı dene.
    except FileNotFoundError as dosyabulunamadi:
        print("Hata..: ",dosyabulunamadi) #Dosya yoksa hata veri.
        return #Komut istemeye geri dön.
    s.sendto(msg.encode(), (HOST, PORT)) #Komutu Servera yolla.
    print(f"{file_name} Servera yükleniyor...")
    DATA_SIZE=os.stat(PATH+"/"+file_name).st_size
    s.sendto(str(DATA_SIZE).encode(),(HOST,PORT))

    data = f.read(BUFFERSIZE)
    while(data):
        if(s.sendto(data, (HOST, PORT))):
            data = f.read(BUFFERSIZE)
            time.sleep(0.002) #Servera dosyayı kaydetmesi için zaman.
    f.close()
    try:
        durum=s.recv(BUFFERSIZE).decode()
    except ConnectionResetError:
        print("Dosya servera yüklenemedi!")
        print("Server bağlantısı sonlandırıldı.")
        exit()
    print(f"{file_name} Gönderildi!")
    print("----------------------------------------------")


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(" ".encode(), (HOST, PORT)) # Bağlandığımızı belli etmek için boş veri yolladık.
data=s.recv(BUFFERSIZE) #Serverdaki dosyalar
print("Bağlantı Kuruldu\n")
print("---------------Kullanım---------------\n")
print("Dosya indirmek için GET dosya_adi.dosya_uzantisi")
print("Dosya yüklemek için PUT dosya_adi.dosya_uzantisi")
print("Çıkmak için EXIT yazın")
print("Serverdaki Dosyalar..:",data.decode())
while True:
    while True:
        komut=str(input("Komut Gir..:"))
        if komut.lower()=="exit":
            s.sendto("exit".encode(),(HOST,PORT))
            exit()
        try:
            komut,dosya=komut.split(" ")
        except:
            print("Hatali Komut Girişi")
            continue
        break
    msg=komut+" "+dosya
    if komut.lower()=="put":
        put(msg,dosya)
        time.sleep(2)
    elif komut.lower()=="get":
        get(msg,dosya)
    else:
        print("Hatali Komut Girişi")
s.close()