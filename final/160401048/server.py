import socket
import time
import datetime

IP = '127.0.0.1'
PORT = 142
BUFFER_SIZE = 1024

TIME_ZONE = "+00"
time_utc = 0
change_utc = input("Server başlamadan UTC değerini değiştirmek ister misiniz?(y/N)")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(1)

if(change_utc.upper().startswith("Y")):
    TIME_ZONE = input("Yeni utc değerini giriniz(örneğin: +03): ")
    if(TIME_ZONE.startswith("+")):
        time_utc = int(TIME_ZONE[1:])*60*60
    else:
        time_utc = int(TIME_ZONE[1:])*60*60*(-1)

print("Server Listening ...")


conn, addr = server_socket.accept()
print('Connection address:', addr)
conn.send((str(time.mktime(time.gmtime()) + time_utc) + "#" + TIME_ZONE).encode())

close = True
while close:
    komut = conn.recv(BUFFER_SIZE)
    if(komut.decode().upper().startswith("GET") or komut.decode().upper().startswith("SET")):
        conn.send((str(time.mktime(time.gmtime()) + time_utc) + "#" + TIME_ZONE).encode())
    else:
        server_socket.close()
        close = False


server_socket.close()