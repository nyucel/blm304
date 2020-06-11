

#----Şamil--GÜVEN--160401038---- 

import socket
import os

host = input("Bağlanılacak Server IP  Giriniz : ")
port = 142

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.send(bytes("gecikme", encoding='utf-8'))
    test = s.recv(128)
    s.send(bytes("istek", encoding='utf-8'))
    zaman = s.recv(128)
    print(zaman)
    os.system('date --set "%s" +\"%%A %%d %%B %%Y %%H:%%M:%%S.%%6N\"' % zaman.decode("utf-8"))
    s.close()
