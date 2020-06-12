#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ad Soyad:  Onur ETLİĞLU - (180401117)
"""

import socket
import sys, os, time
from datetime import  datetime
from datetime import timezone
from datetime import timedelta

HOST = '127.0.0.1'  
PORT = 142          
ZDILIMI = "UTC-2"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server is running...")
    while True:
        conn, addr = s.accept()
        with conn:
            print('Request from:', addr)
            data = conn.recv(1024)
            utc = datetime.now(timezone.utc).timestamp() + (int(ZDILIMI[3:])*3600)
            utc = utc*1000
            z_cevap = str(utc) + "-" + ZDILIMI
            print("UTC Zamanı: "+ str(datetime.now(timezone.utc)))
            conn.sendall(z_cevap.encode())
