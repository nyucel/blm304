import socket
import time
import datetime

ip = '127.0.0.1'
port = 142

t_dilim = "UTC+3"     #ayarlamak istedigimiz zaman dilimi
time_utc = int(t_dilim[3:])*60*60

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.bind((ip, port))
s_socket.listen(1)

print("Server Listening ...")


conn, addr = s_socket.accept()
print('Connection address:', addr)
conn.send((str(time.mktime(time.gmtime()) + time_utc) + "/" + t_dilim).encode())
#istemciye server in bulundugu yerdeki zaman bilgisi gönderildi

close = True
while close:
    komut = conn.recv(1024)
    conn.send((str(time.mktime(time.gmtime()) + time_utc) + "/" + t_dilim).encode())
    
s_socket.close()
