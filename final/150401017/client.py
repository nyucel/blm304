import socket
import subprocess
import shlex
import time


def gecikme(client_time, gecikme_süresi):
    client_time = client_time+gecikme_süresi
    return client_time

def set_time(date):
    subprocess.call(shlex.split("timedatectl set-ntp false"))
    subprocess.call(shlex.split("sudo date -s '" + time.ctime(date) + "'"))
    subprocess.call(shlex.split("sudo hwclock -w"))


ip = '127.0.0.1'
port = 142
adres=(ip,port)

c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #soket olusturuldu
c_socket.connect(adres)     

data = c_socket.recv(1024)
client_time, client_utc = data.decode().split("/")

print("Serverdan gelen saat(UTC+3)= ", time.ctime(float(client_time)), client_utc)

close = True
while close:
    basla = time.time()
    server_time = c_socket.recv(1024)
    client_time, client_utc = server_time.decode().split("/")
    bitir = time.time()
    client_time = gecikme(float(client_time), (basla-bitir))
    set_time(client_time)

c_socket.close()
