import socket
import sys
import time
import os
from datetime import datetime

server_address = ('0.0.0.0', 142)
sock.bind(server_address)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.listen(1)

while True:
    try:
        connection, client_address = sock.accept()

    try:

        while True:
            data = connection.recv(1024)

            if data == b'getmetime':
                format(data)
                time.tzset()
                timeZone = time.tzname
                data = str(time.time()) + ',' + str(timeZone[0])
                bytesdata = bytes(data, 'utf-8')
                connection.sendall(bytesdata)
            else:
                break
    except KeyboardInterrupt:
        print("Durduruldu!")
        sock.close()
        break
    except:
        socket.close()
        print("Hata")
        break
    finally:
        connection.close()