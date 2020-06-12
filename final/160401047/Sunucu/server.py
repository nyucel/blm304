#Batuhan Bagceci - 160401047

import socket
import datetime
import threading

HOST = "0.0.0.0"
PORT = 142

TIMEZONE = "UTC+3"

if((len(TIMEZONE) == 3)):
	TZ = 0
else:
	TZ = int(TIMEZONE[3:])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Sunucu calismaya basladi...")

def handle(conn):
	conn , client = conn

	while(True):
		data = conn.recv(1024)

		if(data.decode() == "1"):
			TIME = ((datetime.datetime.utcnow().timestamp()) + 3600 * TZ) * 1000
			conn.send((str(TIME) + "@" + TIMEZONE).encode())

		if(data.decode() == "0"):
			break

while(True):
	threading.Thread(target=handle, args=(server.accept(),)).start()

server.close()
