#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
    ========================= Veri Haberleşmesi Final Ödevi ========================
    İsim ve Soyisim: Augusto GOMES JUNIOR
    Ögrenci_No: 130401074
"""

import socket
import sys, os, time
from datetime import  datetime
from datetime import timezone
from datetime import timedelta

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 142          # Port to listen on (non-privileged ports are > 1023)
ZAMAN_DILIMI = "UTC+4"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Sunucu Çalışıyor...")
    print("Zaman dilimi: "+ZAMAN_DILIMI)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024)
            utc = datetime.now(timezone.utc).timestamp() + (int(ZAMAN_DILIMI[3:])*60*60)
            utc = utc*1000
            z_cevap = str(utc) + "-" + ZAMAN_DILIMI
            print("UTC Zamanı: "+ str(datetime.now(timezone.utc)))
            conn.sendall(z_cevap.encode())
