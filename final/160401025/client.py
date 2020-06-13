# -*- coding: utf-8 -*-
"""

@author: Halil İbrahim Koç
            Öğrenci No: 160401025
"""

import socket
import os

host = input("Lütfen Server IP adresini giriniz: ")
port = 142

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:

    soc.connect((host, port))
    soc.send(bytes("latency", encoding='utf-8'))
    test = soc.recv(128)
    soc.send(bytes("request", encoding='utf-8'))

    time = soc.recv(128)
    print(time)
    os.system('date --set "%s" +\"%%A %%d %%B %%Y %%H:%%M:%%S.%%6N\"' % time.
              decode("utf-8"))

    soc.close()
