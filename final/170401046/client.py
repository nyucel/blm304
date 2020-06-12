import socket
import datetime
import sys
import time
from timeit import default_timer as timer
import os


server_address = ("192.168.1.32", 142)
message = "can i get time"
A = message.encode("utf-8")
client_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

client_sock.connect(server_address)

client_sock.sendall(A)
gecikme_baslat = timer()
data = client_sock.recv(1024)
gecikme_bitir = timer()
gecikme = (gecikme_baslat-gecikme_bitir) * 1000
data = data.decode("utf-8")
data_list = data.split()

time_period = data_list[1]
print(time_period)

milliseconds = int(data_list[0]) + gecikme
time = milliseconds / 1000.0
year = datetime.datetime.fromtimestamp(time).strftime('%Y')
month = datetime.datetime.fromtimestamp(time).strftime('%m')
day = datetime.datetime.fromtimestamp(time).strftime('%d')
hour = datetime.datetime.fromtimestamp(time).strftime('%H')
minute = datetime.datetime.fromtimestamp(time).strftime('%M')
second = datetime.datetime.fromtimestamp(time).strftime('%S')

date = year + "/" + month + "/" + day
time = hour + ":" + minute + ":" + second
komut = 'sudo date -s '+'"'+str(date)+' '+str(time)+'"'
os.system(komut)

client_sock.close()
