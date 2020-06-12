# BerkantDuman 160401048
import socket
import subprocess
import shlex
import time


def gecikme(c_time, gecikme_süresi):
    c_time += gecikme_süresi
    return c_time


def set_time(date):
    subprocess.call(shlex.split("timedatectl set-ntp false"))
    subprocess.call(shlex.split("sudo date -s '" + time.ctime(date) + "'"))
    subprocess.call(shlex.split("sudo hwclock -w"))


IP = input("Sunucunun IP adresini giriniz: ")
PORT = 142
BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

data = client_socket.recv(BUFFER_SIZE)
c_time, c_utc = data.decode().split("#")

print("Saat - UTC: ", time.ctime(float(c_time)), c_utc)

close = True
while close:
    komut = str(input("Gerçekleştirmek istediğiniz komutu giriniz(GET, SET, Q(quit)): "))
    client_socket.send(komut.encode())
    gecikme_start = time.time()
    if(komut.upper().startswith("GET")):
        server_time = client_socket.recv(BUFFER_SIZE)
        c_time, c_utc = server_time.decode().split("#")
        gecikme_end = time.time()
        c_time = gecikme(float(c_time), (gecikme_end - gecikme_start))
        print("Saat - UTC ", time.ctime(float(c_time)), c_utc)
    elif (komut.upper().startswith("SET")):
        server_time = client_socket.recv(BUFFER_SIZE)
        c_time, c_utc = server_time.decode().split("#")
        gecikme_end = time.time()
        c_time = gecikme(float(c_time), (gecikme_end - gecikme_start))
        set_time(c_time)
    else:
        client_socket.close()
        close = False


client_socket.close()
