# -*- coding: utf-8 -*-
"""
@author: Halil İbrahim Koç
           Öğrenci No: 160401025

"""

import socket
import time
from datetime import datetime, timezone, timedelta
import sys


UTC = +3
port = 142


host = input("Lütfen Server IP giriniz : ")


def latencyTime(client):
    firstT = datetime.utcnow() + timedelta(hours=UTC)
    client.send(bytes(str(firstT), encoding='utf-8'))
    check = client.recv(128)
    lastT = datetime.utcnow() + timedelta(hours=UTC)
    latency = (lastT - firstT) / 2
    print("Gecikme:", latency)
    return latency


with socket.socket() as soc:
    try:

        soc.bind((host, port))
    except:
        print("HATA: Sunucu olusturma başarısız. Tekrar deneyiniz..")
        sys.exit()

    print("------- Sunucu çalışıyor -------")
    while True:

        soc.listen()
        con, addr = soc.accept()
        with con:

            while True:
                data = con.recv(128)

                if not data:
                    break
                latency = latencyTime(con)
                time = datetime.utcnow() + timedelta(hours=UTC) + latency
                con.send(bytes(str(time), encoding='utf-8'))
 
    soc.close()
