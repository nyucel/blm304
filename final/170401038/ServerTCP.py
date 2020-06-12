import socket
import time

host_address = input("Server IP Giriniz : ")
port_number = 142
buffer_size = 1024

utc = input("Lütfen bir zaman dilimi değeri giriniz : ")
time_zone = "UTC+" + utc
tsc = 0

if (time_zone[4:].startswith("+")):
    tsc = int(time_zone[5:]) * 60 * 60 * 1000
else:
    tsc = int(time_zone[5:]) * 60 * 60 * 1000 * (-1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((host_address, port_number))

except:
    print("Sunucuya bağlanılamadı.. Program sonlandırılıyor..")
    exit(1)

print("Sunucu ile bağlantı sağlandı. ")
server_socket.listen(1)

conn, client_addr = server_socket.accept()
print("Bağlantı adresi = ", client_addr)

control = True
while control:
    komut = conn.recv(buffer_size).decode()
    if(komut.upper().startswith("GET") or komut.upper().startswith("SET")):
        conn.send((str(time.mktime(time.gmtime()) + tsc) + "/" + time_zone[4:]).encode())
    else:
        server_socket.close()
        control = False