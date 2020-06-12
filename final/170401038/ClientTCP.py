import socket
import subprocess
import shlex
import time

def gecikmeHesapla(c_time, gecikme_süresi):
    c_time += gecikme_süresi
    return c_time


def zamaniAyarla(date):
    subprocess.call(shlex.split("timedatectl set-ntp false"))
    subprocess.call(shlex.split("sudo date -s '" + time.ctime(date) + "'"))
    subprocess.call(shlex.split("sudo hwclock -w"))


host_address = input("Bağlanılacak IP adresini giriniz : ")
port_number = 142
buffer_size = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_address, port_number))

data = client_socket.recv(buffer_size)
c_time, c_utc = data.decode().split("/")

print("Saat - UTC: ", time.ctime(float(c_time)), c_utc)

control = True
while control:
    komut = str(input("Gerçekleştirmek istediğiniz komutu giriniz(GET, SET): "))
    client_socket.send(komut.encode())
    gecikmeBaslangici = time.time()

    if(komut.upper().startswith("GET")):
        server_time = client_socket.recv(buffer_size)
        c_time, c_utc = server_time.decode().split("/")
        gecikmeSonu = time.time()
        c_time = gecikmeHesapla(float(c_time), (gecikmeSonu - gecikmeBaslangici))
        print("Saat - UTC ", time.ctime(float(c_time)), c_utc)

    elif (komut.upper().startswith("SET")):
        server_time = client_socket.recv(buffer_size)
        c_time, c_utc = server_time.decode().split("/")
        gecikmeSonu = time.time()
        c_time = gecikmeHesapla(float(c_time), (gecikmeSonu - gecikmeBaslangici))
        zamaniAyarla(c_time)

    else:
        control = False

client_socket.close()