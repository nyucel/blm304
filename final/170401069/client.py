import socket
import subprocess
import shlex
import datetime
import time


# Bağlanılacak adres ve port
host = "192.168.1.109"
port = 142

def tarih_olustur(tarih):
    f = open("tarih.txt","w")
    f.write("date -s '")
    f.write(tarih)
    f.write("'")
    f.close()
    degis=open("tarih.txt")
    subprocess.call(shlex.split("sudo timedatectl set-ntp true"))
    subprocess.call(shlex.split(degis))
    subprocess.call(shlex.split("sudo hwclock -w"))

# Socket oluşturulması
client= socket.socket(socket.AF_INET,socket.SOCK_STREAM)          

try:
    # Bağlantıyı yap
    client.connect((host, port)) 
    # serverden yanıtı al
    gelenmesaj = client.recv(1024).decode()
    print(gelenmesaj) 
 
     
    gelen_m = client.recv(1024).decode()
    #milisaniye = milisaniye.decode()
    print("Sunucu Milisaniye => ",gelen_m)
    liste=[]
    liste = gelen_m.split()
   
    milisaniye = (int(liste[0])) / 1000.0
    son = datetime.datetime.fromtimestamp(milisaniye).strftime('%d %b %Y %H:%M:%S')
    tarih_olustur(son)
    
    milisecond = int(round(time.time()*1000))
    milisecond = str(milisecond)
    client.send(milisecond.encode())
    

    #gecikmeli gelen
    gecikmeli = client.recv(1024).decode()
    print("gecikmeli =>",gecikmeli)
    gecikmeli = int(gecikmeli)
    milisaniye = (gecikmeli) / 1000.0
    son_t = datetime.datetime.fromtimestamp(milisaniye).strftime('%d %b %Y %H:%M:%S')
    tarih_olustur(son_t)
    
    

    # bağlantıyı kapat
    client.close() 
except socket.error as msg:
    print("[Server aktif değil.] Mesaj:", msg)
