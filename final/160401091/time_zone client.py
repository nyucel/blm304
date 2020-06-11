import socket
import subprocess
import shlex
import time

# Server IP ve PORT bilgisi:
IP = '127.0.0.1'
PORT = 142
BUFFER_SIZE = 1024

# Bağlantı yapılıyor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

data = client_socket.recv(BUFFER_SIZE)
(c_time, c_utc) = data.decode().split('#')

# Mevcut saat dilimi
print ('Current UTC: ', time.ctime(float(c_time)), c_utc)

close = True

while close:

    # Komutların alınması
    command = str(input('/*------Commands:-----*/\nGET: Get timezone from server \nSET: Set timezone\n/*--------------------*/\n\nYour Input:'))

    # Komutların gönderilmesi
    client_socket.send(command.encode())
    
    # Gecikme
    delay_start = time.time()


    # Komutları Handle Etme
    if command.upper().startswith('GET'):

        # Zaman dilimi alma
        server_time = client_socket.recv(BUFFER_SIZE)
        (c_time, c_utc) = server_time.decode().split('#')

        delay_end = time.time()
        c_time = delay(float(c_time), delay_end - delay_start)

        print ('UTC ', time.ctime(float(c_time)), c_utc)

    elif command.upper().startswith('SET'):

        # Zaman dilimi gönderme
        server_time = client_socket.recv(BUFFER_SIZE)
        (c_time, c_utc) = server_time.decode().split('#')

        delay_end = time.time()
        c_time = delay(float(c_time), delay_end - delay_start)

        set_time(c_time)

    else:

        # Bağlantı sonlandırma
        client_socket.close()
        close = False

client_socket.close()

def delay(c_time, delay_time):
    c_time += delay_time
    return c_time

def set_time(date):
    subprocess.call(shlex.split("timedatectl set-ntp false"))
    subprocess.call(shlex.split("sudo date -s '" + time.ctime(date) + "'"))
    subprocess.call(shlex.split("sudo hwclock -w"))