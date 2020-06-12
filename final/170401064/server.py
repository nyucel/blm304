# -*- coding: utf-8 -*-
import socket
import sys
import time
import os

if os.geteuid() != 0:
    exit("sudo ile çalıştırın")

useDefaultTimeZone = True

if(useDefaultTimeZone == False): # varsayılan zaman dilimini kullanmak istemezsek
    os.environ['TZ'] = 'Etc/GMT+7' # Uygun zaman dilimi değerlerini README.md dosyasından görebiliriz
    time.tzset()

# TCP/IP socket oluşturuluyor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Soket bağlantı noktasına bağlanıyor
server_address = ('0.0.0.0', 142)
print('{}:{} üzerinden başlatıldı'.format(*server_address))
sock.bind(server_address)

# Gelen bağlantılar dinleniyor
sock.listen(1)

while True:
    try:
        print('Bağlantı Bekleniyor')
        connection, client_address = sock.accept()
    except KeyboardInterrupt:
        print("Server Durduruldu!")
        sock.close()
        break
    try:
        print('Gelen bağlantı', client_address)

        while True:
            data = connection.recv(1024)
            
            if data == b'getmetime':
                print('Alınan {!r}'.format(data))
                time.tzset()
                timeZone = time.tzname
                data = str(time.time()) + ',' + str(timeZone[0])
                bytesofdata = bytes(data, 'utf-8')
                print('Yanıt gönderildi', data)
                connection.sendall(bytesofdata)
            else:
                #print('Gelen veri yok', client_address)
                break
    except:
        socket.close()
        print("Sorun oluştu")
        break
    finally:
        # Bağlantıyı temizle
        connection.close()
