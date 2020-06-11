import socket
import time
import datetime

# Server IP ve PORT bilgisi:
IP = '127.0.0.1'
PORT = 142
BUFFER_SIZE = 1024

# Başlangıçtaki dilimi +00
time_zone = '+00'
time_utc = 0

# Değişim Yapılacak mı?
change_utc = input('Do u want to change current timezone? - Current [UTC' + time_zone + '] (y/n)')

# Bağlantı yapılıyor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(1)

# Eğer zaman dilimi değiştirilmek isteniyorsa
if change_utc.upper().startswith('Y'):
    time_zone = input('Set UTC timezone (ex. +03)')
    if time_zone.startswith('+'):
        time_utc = int(time_zone[1:]) * 60 * 60
    else:
        time_utc = int(time_zone[1:]) * 60 * 60 * -1

print 'Server Listening ...'

# Client ile bağlantı sağlanıyor
(conn, addr) = server_socket.accept()
print ('Connection address:', addr)
conn.send((str(time.mktime(time.gmtime()) + time_utc) + '#'
          + time_zone).encode())

close = True
while close:
    command = conn.recv(BUFFER_SIZE)
    if command.decode().upper().startswith('GET') \
        or command.decode().upper().startswith('SET'):
        conn.send((str(time.mktime(time.gmtime()) + time_utc) + '#'
                  + time_zone).encode())
    else:
        server_socket.close()
        close = False

server_socket.close()