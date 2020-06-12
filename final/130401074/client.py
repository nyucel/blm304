#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
    ========================= Veri Haberleşmesi Final Ödevi ========================
    İsim ve Soyisim: Augusto GOMES JUNIOR
    Ögrenci_No: 130401074
"""


import socket
import sys, time
import os
IP = "127.0.0.1"
PORT = 142

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print ("=================== HOŞ GELDİNİZ ==================")
print (" ========== TCP Kullanilan NTP Programi =========== \n")
address = input("Host(127.0.0.1): ")

if not address:
    address = IP

port = input("Port(142): ")

if not port:
    port = PORT
    print ("Baglanti kuruluyor... \n")
    time.sleep(1)

def zaman_ayarla(time_string):
        os.system("sudo timedatectl set-ntp false ")
        os.system("sudo date -s '%s' >> /dev/null " % time_string)
        print("Zaman Ayarlanmştır.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((address, int(port)))
    baslangic_z = time.time()
    s.sendall(b'Zaman')
    data = s.recv(1024)
    bitis_z = time.time()
    gecikme_z = bitis_z - baslangic_z
    gecikme_z = gecikme_z / 2
    data = data.decode().split("-")
    print(data[0])
    zaman = (float(data[0])/1000) + gecikme_z
    t_z = time.gmtime(zaman)
    print("Yerel zaman: ",end="")
    print("%s-%s-%s  %s:%s:%s"%(t_z.tm_year,t_z.tm_mon,t_z.tm_mday,t_z.tm_hour,t_z.tm_min,t_z.tm_sec))
    zaman_ayarla("%s-%s-%s  %s:%s:%s"%(t_z.tm_year,t_z.tm_mon,t_z.tm_mday,t_z.tm_hour,t_z.tm_min,t_z.tm_sec))

