#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Ufuk KORKMAZ
"""

import socket
import sys, time
import os

HOST = "127.0.0.1"
PORT = 142

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address = input("Host: ")

if not address:
    address = HOST

port = input("Port: ")

if not port:
    port = PORT

def zaman_ayarla(time_string):
        os.system("sudo timedatectl set-ntp false && sudo date -s '%s'" % time_string)
        print("Sistem Yeni Zaman Ayarlanmştır.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((address, int(port)))
    start = time.time()
    s.sendall(b'Zaman')
    data = s.recv(1024)
    end = time.time()
    gecikme = end - start
    gecikme = gecikme / 2
    data = data.decode().split("*")
    zaman = (float(data[0])/1000) + gecikme
    t_z = time.gmtime(zaman)
    print("Yerel zaman: ",end="")
    print("%s/%s/%s  %s:%s:%s"%(t_z.tm_year,t_z.tm_mon,t_z.tm_mday,t_z.tm_hour,t_z.tm_min,t_z.tm_sec))
    zaman_ayarla("%s-%s-%s  %s:%s:%s"%(t_z.tm_year,t_z.tm_mon,t_z.tm_mday,t_z.tm_hour,t_z.tm_min,t_z.tm_sec))

