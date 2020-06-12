#Batuhan :OZALP - 170401074
import socket
import time
import os
import datetime
import subprocess
import shlex

from decimal import Decimal

ip = input("Server ip adresini girin >>")
port = 142
buffer = 1024

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        simdiki_zaman = time.time()
            
        zaman = str(s.recv(buffer).decode())   
        
        zaman = Decimal(zaman)
        zaman *= 1000       #milisaniyeye cevirdik
        print("Serverdan gelen milisaniye cinsinden gecen zaman >>", zaman)

        zaman = int(zaman / 1000)#saniyeye cevirdik

        time.sleep(0.3)
        utc = str(s.recv(buffer).decode())#serverdan  gelen utc degeri
        utc = int(utc)
        if(utc > 0):
            print("Server tarafindaki zaman dilimi >> UTC+%d" %utc)
        else:
             print("Server tarafindaki zaman dilimi >> UTC%d" %utc)
             
             
        utc_saati = zaman 

        time.sleep(0.3)     
        server_istegi = str(s.recv(buffer).decode()) #degisecek zaman diliminin degeri 
        istek_zamani = time.time()
        server_istegi = int(server_istegi)
        print("Istenen zaman dilimi >>", server_istegi)
        gecikme = istek_zamani - simdiki_zaman
        utc_saati = (3600 * server_istegi) + gecikme + utc_saati
        saat = str(time.ctime(utc_saati))

        print("Ayarlanmasi beklenen zaman >>", time.ctime(utc_saati))
        subprocess.call(shlex.split("timedatectl set-ntp false"))
        subprocess.call(shlex.split("sudo date -s '%s'" % saat))
        subprocess.call(shlex.split("sudo hwclock -w"))
    except:
        s.close()
main()














